import platform
import os

class Plugin:
    name = "system_info"

    def match(self, command: str) -> bool:
        keywords = ["system info", "cpu", "ram", "machine"]
        return any(word in command.lower() for word in keywords)

    def run(self, command: str) -> str:
        info = {
            "OS": platform.system(),
            "Release": platform.release(),
            "Machine": platform.machine(),
            "CPU": platform.processor(),
            "Cores": os.cpu_count(),
        }
        return f"[System Info]\n{info}"
