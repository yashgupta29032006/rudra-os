import os

class Plugin:
    name = "list_files"

    def match(self, command: str) -> bool:
        keywords = ["list files", "show files", "ls"]
        return any(k in command.lower() for k in keywords)

    def run(self, command: str) -> str:
        return self.execute(".")

    def execute(self, path: str = ".") -> str:
        try:
            files = os.listdir(path)
            return "[Files]\n" + "\n".join(files)
        except Exception as e:
            return f"[Files] Error: {e}"

    @property
    def schema(self):
        return {
            "path": str
        }
