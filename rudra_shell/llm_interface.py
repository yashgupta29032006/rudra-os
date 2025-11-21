import os
import google.generativeai as genai


class LLMInterface:
    def __init__(self, model_name="gemini-1.5-flash"):
        # Correct key fetch
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY environment variable")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def ask(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[LLM ERROR] {e}"
