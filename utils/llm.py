from groq import Groq
from typing import Optional
import time

from config import Config


class LLMClient:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE

    def generate(self, prompt: str, max_retries: int = 2) -> str:
        """
        Generate response from Groq LLM with retry logic.
        """

        attempt = 0

        while attempt <= max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    temperature=self.temperature,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a strict AI that returns ONLY valid JSON. No explanations."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                return response.choices[0].message.content

            except Exception as e:
                attempt += 1

                if attempt > max_retries:
                    raise RuntimeError(f"LLM failed after retries: {str(e)}")

                # 🔁 small delay before retry
                time.sleep(1)