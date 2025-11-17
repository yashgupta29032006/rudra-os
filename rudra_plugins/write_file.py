class Plugin:
    name = "write_file"

    def match(self, command: str) -> bool:
        return "write" in command.lower() and " to " in command.lower()

    def run(self, command: str) -> str:
        try:
            parts = command.split(" to ")
            text = parts[0].replace("write", "").strip()
            filename = parts[1].strip()

            with open(filename, "a") as f:
                f.write(text + "\n")

            return f"[File] Wrote to {filename}: {text}"
        except Exception as e:
            return f"[File] Error: {e}"
