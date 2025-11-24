class Plugin:
    name = "write_file"

    def match(self, command: str) -> bool:
        return "write" in command.lower() and " to " in command.lower()

    def run(self, command: str) -> str:
        try:
            parts = command.split(" to ")
            text = parts[0].replace("write", "").strip()
            filename = parts[1].strip()
            return self.execute(filename, text)
        except Exception as e:
            return f"[File] Error: {e}"

    def execute(self, path: str, content: str) -> str:
        try:
            with open(path, "a") as f:
                f.write(content + "\n")
            return f"[File] Wrote to {path}: {content}"
        except Exception as e:
            return f"[File] Error: {e}"

    @property
    def schema(self):
        return {
            "path": str,
            "content": str
        }
