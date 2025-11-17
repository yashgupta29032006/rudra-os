class AgentPlanner:
    def __init__(self):
        print("Agent Planner Ready.")

    def plan(self, prompt: str):
        prompt = prompt.lower()

        steps = []

        if "create a folder" in prompt:
            parts = prompt.split("create a folder")
            folder = parts[1].strip().split()[0]
            steps.append({
                "tool": "folder",
                "args": { "command": f"create folder {folder}" }
            })

        if "create a file" in prompt:
            parts = prompt.split("create a file")
            file = parts[1].strip().split()[0]
            steps.append({
                "tool": "create_file",
                "args": { "command": f"create file {file}" }
            })

        if "write" in prompt and "to" in prompt:
            try:
                before, after = prompt.split("to")
                text = before.replace("write", "").strip()
                filename = after.strip().split()[0]
                steps.append({
                    "tool": "write_file",
                    "args": { "command": f"write {text} to {filename}" }
                })
            except:
                pass
        
        if steps:
            return steps

        return [{
            "tool": "None",
            "args": {}
        }]
