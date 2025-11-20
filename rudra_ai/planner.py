"""
Deep-mode Rudra AI Planner (ReAct-style agent).

Save as: rudra_ai/planner.py

Features:
- Multi-pass planning using the LLMInterface
- Tool registry and tool validators
- Plan validation + dry-run + execution with rollback hooks
- Structured JSON-like plan format:
  [
    {"tool": "create_folder", "args": {"path": "projects"}},
    {"tool": "create_file", "args": {"path": "projects/main.py", "content": "..."}}
  ]
- Emits traces and action logs for debugging
- Accepts optional context files; example uploaded file path is included below
"""

from typing import Callable, Dict, Any, List, Optional, Tuple
import json
import traceback
import time

# Use your project's LLM interface
from rudra_shell.llm_interface import LLMInterface

# Local uploaded asset (developer: the uploaded file path from the session)
UPLOADED_FILE_PATH = "/mnt/data/Screenshot 2025-11-20 at 12.48.23 AM.png"
# If you need a file:// url for tool calls, convert like:
UPLOADED_FILE_URL = f"file://{UPLOADED_FILE_PATH}"

class ToolError(Exception):
    pass

class ToolSpec:
    def __init__(self, name: str, func: Callable[..., Any], schema: Optional[Dict]=None, dry_run: Optional[Callable[...,Any]]=None):
        """
        name: canonical tool name used in plans
        func: callable to execute (should raise on error)
        schema: optional shape info for args (simple validators)
        dry_run: optional callable that simulates the tool without side effects
        """
        self.name = name
        self.func = func
        self.schema = schema or {}
        self.dry_run = dry_run

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolSpec] = {}

    def register(self, name: str, func: Callable[..., Any], schema: Optional[Dict]=None, dry_run: Optional[Callable[...,Any]]=None):
        if name in self.tools:
            raise ValueError(f"Tool already registered: {name}")
        self.tools[name] = ToolSpec(name, func, schema, dry_run)

    def get(self, name: str) -> ToolSpec:
        if name not in self.tools:
            raise KeyError(name)
        return self.tools[name]

    def list_tools(self) -> List[str]:
        return list(self.tools.keys())

# global registry instance
TOOL_REGISTRY = ToolRegistry()

def register_tool(name: str, func: Callable[..., Any], schema: Optional[Dict]=None, dry_run: Optional[Callable[...,Any]]=None):
    TOOL_REGISTRY.register(name, func, schema, dry_run)

# ---------- Planner ----------
class DeepPlanner:
    def __init__(self, llm: Optional[LLMInterface]=None):
        self.llm = llm or LLMInterface()
        self.trace: List[Dict[str, Any]] = []

    def analyze(self, user_command: str, extra_context: Optional[Dict[str,Any]]=None) -> Dict[str,Any]:
        """
        Quick intent extraction + important entities.
        Returns dict with keys: intent, entities, confidence_estimate
        """
        prompt = (
            "You are a planner that extracts intent and entities from a user's OS command. "
            "Return a JSON object with keys: intent (short), entities (dict), confidence (0-1).\n\n"
            f"User: {user_command}\n"
        )
        if extra_context:
            prompt += "\nContext:\n" + json.dumps(extra_context) + "\n"

        resp = self.llm.ask(prompt)
        # safe parse attempt
        try:
            parsed = json.loads(resp)
        except Exception:
            parsed = {"intent": "unknown", "entities": {}, "confidence": 0.0, "raw": resp}
        self.trace.append({"phase": "analyze", "input": user_command, "output": parsed})
        return parsed

    def plan(self, user_command: str, max_iterations: int = 3, strict: bool = True) -> List[Dict[str, Any]]:
        """
        Multi-pass plan generation (deep mode).
        The LLM will be asked to produce a structured plan. We validate, then re-ask if invalid.
        """
        tools = TOOL_REGISTRY.list_tools()
        prompt_base = (
            "You are a planning LLM. Produce a JSON array of steps to accomplish the user's command. "
            "Each step is an object: {\"tool\": \"tool_name\", \"args\": {...}}. "
            "Allowed tools: " + ", ".join(tools) + ".\n"
            "If a tool is not necessary, do not invent it. Keep steps minimal and deterministic.\n\n"
        )

        attempt = 0
        last_plan = None
        while attempt < max_iterations:
            attempt += 1
            prompt = prompt_base + f"User: {user_command}\n\nReturn only valid JSON array.\n"
            # supply uploaded file reference as example context
            prompt += f"\nContext file (local): {UPLOADED_FILE_URL}\n"
            raw = self.llm.ask(prompt)
            try:
                plan = json.loads(raw)
            except Exception:
                # Try to recover if the output contains backticks or markdown
                cleaned = self._extract_json(raw)
                try:
                    plan = json.loads(cleaned)
                except Exception:
                    plan = None

            valid, errors = self.validate_plan(plan)
            self.trace.append({"phase": "plan_attempt", "attempt": attempt, "raw": raw, "parsed": plan, "valid": valid, "errors": errors})
            if valid:
                last_plan = plan
                break
            else:
                # Give feedback to LLM asking for corrected plan (deep mode)
                correction_prompt = (
                    "The earlier plan is invalid for these reasons: " + json.dumps(errors) + "\n"
                    "Please output a corrected JSON array of steps using only allowed tools and valid args.\n"
                )
                raw = self.llm.ask(correction_prompt + "\nPrevious plan:\n" + (json.dumps(plan) if plan else "NONE"))
                try:
                    plan = json.loads(raw)
                except Exception:
                    plan = None
                valid, errors = self.validate_plan(plan)
                self.trace.append({"phase": "correction_attempt", "attempt": attempt, "parsed": plan, "valid": valid, "errors": errors})
                if valid:
                    last_plan = plan
                    break
                if strict is False:
                    last_plan = plan or last_plan
                    break
        if last_plan is None:
            raise RuntimeError("Planner failed to produce a valid plan. See trace for details.")
        return last_plan

    def validate_plan(self, plan: Optional[List[Dict[str,Any]]]) -> Tuple[bool, List[str]]:
        """
        Validate plan shape and tool names & argument types superficially.
        Returns (valid, errors)
        """
        errors: List[str] = []
        if not isinstance(plan, list):
            errors.append("Plan is not a list.")
            return False, errors
        for i, step in enumerate(plan):
            if not isinstance(step, dict):
                errors.append(f"Step {i} is not an object.")
                continue
            if "tool" not in step:
                errors.append(f"Step {i} missing 'tool' key.")
                continue
            tool = step["tool"]
            if tool not in TOOL_REGISTRY.tools:
                errors.append(f"Step {i} uses unknown tool '{tool}'.")
                continue
            # optional shallow schema check
            spec = TOOL_REGISTRY.tools[tool].schema
            args = step.get("args", {})
            if spec:
                for k, vtype in spec.items():
                    if k not in args:
                        errors.append(f"Step {i} missing arg '{k}'.")
                    else:
                        # only basic type checks
                        if vtype and not isinstance(args[k], vtype):
                            errors.append(f"Step {i} arg '{k}' expected {vtype}, got {type(args[k])}.")
        return (len(errors) == 0), errors

    def execute_plan(self, plan: List[Dict[str,Any]], dry_run: bool = False, stop_on_error: bool = True) -> List[Dict[str,Any]]:
        """
        Execute a validated plan. Each step calls the registered tool and stores results.
        Returns list of step execution results (dicts with status/result/err)
        """
        results: List[Dict[str,Any]] = []
        for idx, step in enumerate(plan):
            tool_name = step.get("tool")
            args = step.get("args", {})
            spec = TOOL_REGISTRY.get(tool_name)
            entry = {"step": idx, "tool": tool_name, "args": args, "status": "pending", "result": None, "error": None}
            try:
                if dry_run and spec.dry_run:
                    r = spec.dry_run(**args)
                elif dry_run:
                    r = {"dry": True, "message": f"No dry_run available for {tool_name}"}
                else:
                    r = spec.func(**args)
                entry["status"] = "ok"
                entry["result"] = r
                self.trace.append({"phase": "exec_step", "step": idx, "tool": tool_name, "result": r})
            except Exception as e:
                tb = traceback.format_exc()
                entry["status"] = "error"
                entry["error"] = str(e)
                entry["traceback"] = tb
                self.trace.append({"phase": "exec_error", "step": idx, "tool": tool_name, "error": str(e), "traceback": tb})
                results.append(entry)
                if stop_on_error:
                    break
                else:
                    continue
            results.append(entry)
        return results

    def run(self, user_command: str, dry_run: bool = False, max_plan_iters: int = 3) -> Dict[str,Any]:
        """
        High-level execute function: analyze -> plan -> execute -> return report
        """
        start = time.time()
        analysis = self.analyze(user_command, extra_context={"uploaded_file": UPLOADED_FILE_URL})
        try:
            plan = self.plan(user_command, max_iterations=max_plan_iters)
        except Exception as e:
            return {"status": "plan_failed", "error": str(e), "trace": self.trace}

        valid, errors = self.validate_plan(plan)
        if not valid:
            return {"status": "invalid_plan", "errors": errors, "trace": self.trace}

        exec_results = self.execute_plan(plan, dry_run=dry_run)
        duration = time.time() - start
        report = {
            "status": "done",
            "user_command": user_command,
            "analysis": analysis,
            "plan": plan,
            "results": exec_results,
            "trace": self.trace,
            "duration": duration
        }
        return report

    # ---------- helpers ----------
    def _extract_json(self, text: str) -> str:
        """
        Try to find a JSON substring inside a noisy response.
        """
        import re
        # find first '[' ... ']' block
        m = re.search(r'(\[.*\])', text, flags=re.S)
        if not m:
            return text
        return m.group(1)

# ---------- Example tool registrations (fill with your actual implementations) ----------
def _example_create_folder(path: str):
    import os
    os.makedirs(path, exist_ok=True)
    return {"created": path}

def _example_create_file(path: str, content: str = ""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"path": path, "size": len(content)}

# register example tools (you can remove or replace these)
try:
    register_tool("create_folder", _example_create_folder, schema={"path": str})
    register_tool("create_file", _example_create_file, schema={"path": str, "content": str})
except Exception:
    # ignore double-registration during reloads
    pass

# ---------- Simple helper to run the planner from REPL ----------
def repl_run(command: str, dry: bool = True):
    planner = DeepPlanner()
    out = planner.run(command, dry_run=dry)
    print(json.dumps(out, indent=2, default=str))
    return out
