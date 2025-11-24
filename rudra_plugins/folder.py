import os

class Plugin:
    name = "folder"

    def match(self, command: str) -> bool:
        keywords = ["create folder", "make folder", "new folder", "mkdir"]
        return any(word in command.lower() for word in keywords)

    def run(self, command: str) -> str:
        parts = command.split()
        folder = parts[-1] 
        return self.execute(folder)

    def execute(self, path: str) -> str:
        try:
            os.makedirs(path, exist_ok=True)
            return f"[Folder] Created folder: {path}"
        except Exception as e:
            return f"[Folder] Error: {e}"

    @property
    def schema(self):
        return {
            "path": str
        }
