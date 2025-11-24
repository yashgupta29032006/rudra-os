import os
import shutil

class Plugin:
    name = "delete"

    def match(self, command: str) -> bool:
        return "delete" in command.lower() or "remove" in command.lower()

    def run(self, command: str) -> str:
        target = command.replace("delete", "").replace("remove", "").strip()
        return self.execute(target)

    def execute(self, path: str) -> str:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                return f"[Delete] Folder removed: {path}"
            elif os.path.isfile(path):
                os.remove(path)
                return f"[Delete] File removed: {path}"
            else:
                return f"[Delete] Not found: {path}"
        except Exception as e:
            return f"[Delete] Error: {e}"

    @property
    def schema(self):
        return {
            "path": str
        }
