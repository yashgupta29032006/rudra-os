class Plugin:
    name = "create_file"

    def match(self, command: str) -> bool:
        keywords = ["create file", "make file", "new file", "touch"]
        return any(k in command.lower() for k in keywords)

    def run(self, command: str) -> str:
        parts = command.split()
        filename = parts[-1]

        try:
            with open(filename, "w") as f:
                f.write("")  # empty file
            return f"[File] Created file: {filename}"
        except Exception as e:
            return f"[File] Error: {e}"
