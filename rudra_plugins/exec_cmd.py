import subprocess

class Plugin:
    name = "exec_cmd"

    def match(self, command: str) -> bool:
        return command.lower().startswith("exec ")

    def run(self, command: str) -> str:
        raw_cmd = command.replace("exec ", "")
        try:
            output = subprocess.getoutput(raw_cmd)
            return "[Exec]\n" + output
        except Exception as e:
            return f"[Exec] Error: {e}"
