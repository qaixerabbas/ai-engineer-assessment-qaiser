import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPERHERO_API_TOKEN = os.getenv("SUPERHERO_API_TOKEN")
GROQ_URL = os.getenv("GROQ_URL")
MODEL = os.getenv("MODEL")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

if not SUPERHERO_API_TOKEN:
    raise RuntimeError("SUPERHERO_API_TOKEN is not set")

if not GROQ_URL:
    raise RuntimeError("GROQ_URL is not set")

if not MODEL:
    raise RuntimeError("MODEL is not set")