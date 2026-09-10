import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

SESSION_DIR = Path(
    "/tmp/csv-auto-cleaner-sessions"
    if os.getenv("VERCEL")
    else BASE_DIR / "sessions"
)

MAX_UPLOAD_SIZE = 100 * 1024 * 1024

SESSION_TTL_SECONDS = 30 * 60

ALLOWED_EXTENSIONS = {
    "csv",
    "xlsx",
    "xls",
    "json",
    "tsv",
}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        SECRET_KEY = "development-only-secret"

    MAX_CONTENT_LENGTH = MAX_UPLOAD_SIZE

    SESSION_DIR = SESSION_DIR

    SESSION_TTL_SECONDS = SESSION_TTL_SECONDS

    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS

    JSON_SORT_KEYS = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.getenv("COOKIE_SECURE", "0") == "1"
    )

    SESSION_COOKIE_PATH = "/"

    PERMANENT_SESSION_LIFETIME = SESSION_TTL_SECONDS