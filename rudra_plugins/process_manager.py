import subprocess
import os

class Plugin:
    name = "process_manager"

    def match(self, command: str) -> bool:
        return command.lower().startswith("ps") or "kill" in command.lower()

    def run(self, command: str) -> str:
        if command.lower().startswith("ps"):
            output = subprocess.getoutput("ps aux")
            return "[Processes]\n" + output

        if "kill" in command.lower():
            parts = command.split()
            try:
                pid = int(parts[-1])
                os.kill(pid, 9)
                return f"[Kill] Process {pid} terminated."
            except Exception as e:
                return f"[Kill] Error: {e}"

        return "[Process Manager] Command not recognized."
