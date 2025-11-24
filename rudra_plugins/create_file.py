class Plugin:
    name = "create_file"

    def match(self, command: str) -> bool:
        keywords = ["create file", "make file", "new file", "touch"]
        return any(k in command.lower() for k in keywords)

    def run(self, command: str) -> str:
        parts = command.split()
        filename = parts[-1]
        return self.execute(filename)

    def execute(self, path: str, content: str = "") -> str:
        try:
            with open(path, "w") as f:
                f.write(content)
            return f"[File] Created file: {path}"
        except Exception as e:
            return f"[File] Error: {e}"

    @property
    def schema(self):
        return {
            "path": str,
            "content": str
        }
