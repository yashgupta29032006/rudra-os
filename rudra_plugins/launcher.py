import subprocess

class Plugin:
    name = "launcher"

    def match(self, command: str) -> bool:
        keywords = ["open", "launch", "run", "start"]
        return any(k in command.lower().split() for k in keywords)

    def run(self, command: str) -> str:
        parts = command.split()
        if len(parts) < 2:
            return "[Launcher] Please specify an application."

        app = parts[-1]
        
        try:
            subprocess.Popen([app])
            return f"[Launcher] Started application: {app}"
        except Exception as e:
            return f"[Launcher] Error: {e}"
