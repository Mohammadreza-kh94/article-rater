import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / ".env"
if env_file.exists():
    load_dotenv(env_file)

DEBUG = os.getenv("DEBUG", "False")
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-j3*8hb3x&8x##w1^kq4%2s5#z20=*a3nv=42i7#5d$2r*#w)kr")

# Database configuration
DATABASE_NAME = os.getenv("DATABASE_NAME", "articlerater_db")
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "1")
