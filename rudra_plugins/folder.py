import os

class Plugin:
    name = "folder"

    def match(self, command: str) -> bool:
        keywords = ["create folder", "make folder", "new folder", "mkdir"]
        return any(word in command.lower() for word in keywords)

    def run(self, command: str) -> str:
        parts = command.split()
        folder = parts[-1] 
        try:
            os.makedirs(folder, exist_ok=True)
            return f"[Folder] Created folder: {folder}"
        except Exception as e:
            return f"[Folder] Error: {e}"
