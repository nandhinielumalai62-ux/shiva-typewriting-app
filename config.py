import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "shiva-commercial-institute-2026-secret")
    INSTITUTE_NAME = "Shiva Commercial Institute"
    INSTITUTE_SUBTITLE = "Government Recognized English & Tamil Typewriting Institute"

    # Database backend: 'mysql' (default) or 'sqlite' (for local offline fallback/tests)
    DB_BACKEND = os.environ.get("DB_BACKEND", "mysql").lower()
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "shiva_typewriting_db")
    SQLITE_PATH = os.environ.get("SQLITE_PATH", str(BASE_DIR / "shiva_typewriting_local.db"))

    # Uploads
    UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads" / "photos")
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4 MB max photo upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Practice & Fee defaults
    PRACTICE_DURATION_SECONDS = int(os.environ.get("DEFAULT_PRACTICE_SECONDS", "600"))  # 10 minutes
    DEFAULT_MONTHLY_FEE = float(os.environ.get("DEFAULT_MONTHLY_FEE", "500"))
    DEFAULT_ADMISSION_FEE = float(os.environ.get("DEFAULT_ADMISSION_FEE", "200"))
    DEFAULT_FEE_DUE_DAY = int(os.environ.get("DEFAULT_FEE_DUE_DAY", "10"))

    COURSE_CATEGORIES = [
        "Junior English Basic",
        "Junior English Speed",
        "Senior English Speed",
        "Junior Tamil Basic",
        "Junior Tamil Speed",
        "Senior Tamil Speed",
    ]

    BATCH_TIMINGS = [
        "07:00 AM - 08:00 AM",
        "08:00 AM - 09:00 AM",
        "09:00 AM - 10:00 AM",
        "10:00 AM - 11:00 AM",
        "11:00 AM - 12:00 PM",
        "12:00 PM - 01:00 PM",
        "01:00 PM - 02:00 PM",
        "02:00 PM - 03:00 PM",
        "03:00 PM - 04:00 PM",
        "04:00 PM - 05:00 PM",
        "05:00 PM - 06:00 PM",
        "06:00 PM - 07:00 PM",
    ]
