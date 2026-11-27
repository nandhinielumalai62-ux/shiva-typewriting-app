import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, time
from decimal import Decimal
from config import Config

try:
    import mysql.connector
    HAS_MYSQL_CONNECTOR = True
except ImportError:
    mysql = None
    HAS_MYSQL_CONNECTOR = False

try:
    import pymysql
    import pymysql.cursors
    HAS_PYMYSQL = True
except ImportError:
    pymysql = None
    HAS_PYMYSQL = False


def get_backend():
    return Config.DB_BACKEND


def _normalize_row(row):
    """Convert database-specific types (Decimal, date/time) consistently."""
    if row is None:
        return None
    out = {}
    for k, v in dict(row).items():
        if isinstance(v, Decimal):
            out[k] = float(v)
        elif isinstance(v, (date, datetime)):
            out[k] = v.isoformat()
        elif isinstance(v, time):
            out[k] = v.strftime("%H:%M:%S")
        else:
            out[k] = v
    return out


class DBConnectionWrapper:
    """Unified DB wrapper supporting MySQL (primary) and SQLite (offline/test)."""

    def __init__(self, conn, backend):
        self.conn = conn
        self.backend = backend

    def _prepare_sql(self, sql):
        if self.backend == "sqlite":
            return sql.replace("%s", "?")
        return sql

    def fetchone(self, sql, params=()):
        q = self._prepare_sql(sql)
        if self.backend == "sqlite":
            cur = self.conn.execute(q, params)
            row = cur.fetchone()
            return _normalize_row(row)
        if self.backend == "mysql_connector":
            cur = self.conn.cursor(dictionary=True)
            cur.execute(q, params)
            row = cur.fetchone()
            cur.close()
            return _normalize_row(row)
        cur = self.conn.cursor()
        cur.execute(q, params)
        row = cur.fetchone()
        cur.close()
        return _normalize_row(row)

    def fetchall(self, sql, params=()):
        q = self._prepare_sql(sql)
        if self.backend == "sqlite":
            cur = self.conn.execute(q, params)
            rows = cur.fetchall()
            return [_normalize_row(r) for r in rows]
        if self.backend == "mysql_connector":
            cur = self.conn.cursor(dictionary=True)
            cur.execute(q, params)
            rows = cur.fetchall()
            cur.close()
            return [_normalize_row(r) for r in rows]
        cur = self.conn.cursor()
        cur.execute(q, params)
        rows = cur.fetchall()
        cur.close()
        return [_normalize_row(r) for r in rows]

    def execute(self, sql, params=()):
        q = self._prepare_sql(sql)
        if self.backend == "sqlite":
            cur = self.conn.execute(q, params)
            return cur.lastrowid
        cur = self.conn.cursor()
        cur.execute(q, params)
        last_id = cur.lastrowid
        cur.close()
        return last_id

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()


def _create_sqlite_schema(conn):
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS staff_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'admin',
            password_hash TEXT NOT NULL,
            phone TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS institute_counters (
            counter_key TEXT PRIMARY KEY,
            last_number INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_code TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            father_guardian_name TEXT NOT NULL,
            guardian_occupation TEXT DEFAULT '',
            gender TEXT NOT NULL,
            dob TEXT NOT NULL,
            qualification TEXT NOT NULL,
            school_college TEXT DEFAULT '',
            phone TEXT NOT NULL,
            alt_phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            address TEXT NOT NULL,
            city TEXT DEFAULT '',
            pincode TEXT DEFAULT '',
            aadhaar_no TEXT DEFAULT '',
            course_category TEXT NOT NULL,
            batch_timing TEXT NOT NULL,
            machine_no TEXT DEFAULT '',
            admission_date TEXT NOT NULL,
            admission_fee REAL NOT NULL DEFAULT 200.0,
            monthly_fee REAL NOT NULL DEFAULT 500.0,
            fee_due_day INTEGER NOT NULL DEFAULT 10,
            photo_filename TEXT DEFAULT '',
            password_hash TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            login_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Present',
            marked_by TEXT NOT NULL DEFAULT 'AUTO_LOGIN',
            practice_category TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (student_id, attendance_date),
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS fee_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            billing_month TEXT NOT NULL,
            amount REAL NOT NULL,
            due_date TEXT NOT NULL,
            paid_date TEXT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            payment_mode TEXT DEFAULT '',
            receipt_no TEXT DEFAULT '',
            intimation_note TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (student_id, billing_month),
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS practice_passages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            practice_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            content_type TEXT NOT NULL DEFAULT 'paragraph',
            passage_text TEXT NOT NULL,
            target_wpm INTEGER NOT NULL DEFAULT 30,
            target_strokes INTEGER NOT NULL DEFAULT 600,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (category, practice_number)
        );

        CREATE TABLE IF NOT EXISTS practice_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            practice_number INTEGER NOT NULL DEFAULT 1,
            content_type TEXT NOT NULL DEFAULT 'paragraph',
            duration_sec INTEGER NOT NULL DEFAULT 0,
            strokes INTEGER NOT NULL DEFAULT 0,
            wpm INTEGER NOT NULL DEFAULT 0,
            accuracy_pct INTEGER NOT NULL DEFAULT 100,
            errors INTEGER NOT NULL DEFAULT 0,
            weak_chars TEXT DEFAULT '',
            target_met INTEGER NOT NULL DEFAULT 0,
            practiced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()


def create_mysql_database_and_tables():
    """Ensure MySQL database and tables exist using configured credentials."""
    if HAS_MYSQL_CONNECTOR:
        root_conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
        )
        cur = root_conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DATABASE}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        root_conn.commit()
        cur.close()
        root_conn.close()
    elif HAS_PYMYSQL:
        root_conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            charset="utf8mb4",
        )
        with root_conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DATABASE}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        root_conn.commit()
        root_conn.close()
    else:
        raise RuntimeError(
            "MySQL driver missing. Install mysql-connector-python: pip install -r requirements.txt"
        )

    from pathlib import Path

    schema_path = Path(__file__).resolve().parent / "sql" / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    with get_db() as db:
        statements = [s.strip() for s in schema_sql.split(";") if s.strip()]
        for stmt in statements:
            upper = stmt.upper()
            if upper.startswith("CREATE DATABASE") or upper.startswith("USE "):
                continue
            db.execute(stmt)
        db.commit()


def open_connection():
    backend = get_backend()
    if backend == "sqlite":
        conn = sqlite3.connect(Config.SQLITE_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return DBConnectionWrapper(conn, "sqlite")

    if HAS_MYSQL_CONNECTOR:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            charset="utf8mb4",
        )
        return DBConnectionWrapper(conn, "mysql_connector")

    if HAS_PYMYSQL:
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return DBConnectionWrapper(conn, "pymysql")

    raise RuntimeError(
        "MySQL driver not installed. Run `pip install -r requirements.txt` "
        "or set DB_BACKEND=sqlite for local testing."
    )


@contextmanager
def get_db():
    db = open_connection()
    try:
        yield db
    finally:
        db.close()


def init_db_schema():
    backend = get_backend()
    if backend == "sqlite":
        conn = sqlite3.connect(Config.SQLITE_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _create_sqlite_schema(conn)
        conn.close()
    else:
        create_mysql_database_and_tables()
