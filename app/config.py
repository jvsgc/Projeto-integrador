# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # carrega .env automaticamente

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()
