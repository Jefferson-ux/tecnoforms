import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = BASE_DIR / "models"

# Astro en desarrollo corre en el puerto 4321
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:4321,http://127.0.0.1:4321"
).split(",")