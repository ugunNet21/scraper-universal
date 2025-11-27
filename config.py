# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
    # Ubah string "True"/"False" jadi boolean Python
    HEADLESS = os.getenv("HEADLESS_MODE", "False").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", 60000))
    
    # Parsing keyword dari koma menjadi list
    KEYWORDS = [k.strip() for k in os.getenv("TARGET_KEYWORDS", "").split(",") if k.strip()]
    CSV_FILE = os.getenv("CSV_FILENAME", "data_scraping.csv")

settings = Config()