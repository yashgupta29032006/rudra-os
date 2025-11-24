class Plugin:
    name = "read_file"

    def match(self, command: str) -> bool:
        return "read file" in command.lower()

    def run(self, command: str) -> str:
        filename = command.lower().replace("read file", "").strip()
        return self.execute(filename)

    def execute(self, path: str) -> str:
        try:
            with open(path, "r") as f:
                content = f.read()
            return f"[File Content]\n{content}"
        except Exception as e:
            return f"[File] Error: {e}"

    @property
    def schema(self):
        return {
            "path": str
        }
