import os
import shutil

class Plugin:
    name = "delete"

    def match(self, command: str) -> bool:
        return "delete" in command.lower() or "remove" in command.lower()

    def run(self, command: str) -> str:
        target = command.replace("delete", "").replace("remove", "").strip()

        try:
            if os.path.isdir(target):
                shutil.rmtree(target)
                return f"[Delete] Folder removed: {target}"
            elif os.path.isfile(target):
                os.remove(target)
                return f"[Delete] File removed: {target}"
            else:
                return f"[Delete] Not found: {target}"
        except Exception as e:
            return f"[Delete] Error: {e}"
