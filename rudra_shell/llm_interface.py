import os
import google.generativeai as genai

class LLMInterface:
    def __init__(self, model_name="gemini-2.0-pro-exp"):
        api_key = os.environ.get("AIzaSyAJ2B1fSSfIGCTLvqrfj737TcgjxC0mkzA")
        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY environment variable")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def chat(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[LLM ERROR] {e}"
