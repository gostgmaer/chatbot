from google.genai import types

from google import genai
from config.config import API_KEY, MODEL
from google.genai.types import Content, Part


class GeminiChatbot:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)

    def ask(self, history: list[Content], system_prompt: str):
        return self.client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )

    def ask_stream(self, history: list[Content], system_prompt: str):
        return self.client.models.generate_content_stream(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
