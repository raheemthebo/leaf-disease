import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing or empty in .env file. Please add a valid Groq API key from https://console.groq.com")

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
MAX_IMAGE_SIZE = 20 * 1024 * 1024
SUPPORTED_FORMATS = ["image/jpeg", "image/png", "image/webp", "image/gif"]
