import subprocess

class Plugin:
    name = "exec_cmd"

    def match(self, command: str) -> bool:
        return command.lower().startswith("exec ")

    def run(self, command: str) -> str:
        raw_cmd = command.replace("exec ", "")
        return self.execute(raw_cmd)

    def execute(self, command: str) -> str:
        try:
            output = subprocess.getoutput(command)
            return "[Exec]\n" + output
        except Exception as e:
            return f"[Exec] Error: {e}"

    @property
    def schema(self):
        return {
            "command": str
        }
