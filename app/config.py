import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = PROJECT_ROOT / "web"
PROMPT_FILE = PROJECT_ROOT / "app" / "prompts" / "extract_tasks.txt"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "240"))
GENERATION_OPTIONS = {"temperature": 0, "num_ctx": 8192, "num_predict": 2048}
