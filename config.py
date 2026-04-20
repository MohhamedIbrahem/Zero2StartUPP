import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    # 🔑 API KEYS
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY")
    FIRECRAWL_API_KEY: str = os.getenv("FIRECRAWL_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "zero2startup"

    # 🤖 LLM SETTINGS
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    TEMPERATURE: float = 0.2

    @classmethod
    def validate(cls):
        missing = []

        for key, value in cls.__dict__.items():
            if key.isupper() and value is None:
                missing.append(key)

        if missing:
            raise ValueError(
                f"❌ Missing environment variables: {', '.join(missing)}"
            )


# Validate on import (fail fast)
Config.validate()