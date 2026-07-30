"""
database.py — SQLite Database Layer
=====================================
Handles all database operations for the AI Resume–JD Matcher.

Schema:
  - users   : id, username (UNIQUE), password (SHA-256 hashed)
  - history : id, username, resume_name, match_score,
              missing_skills, timestamp

CRUD helpers:
  - init_db()           → Creates tables if they don't exist
  - create_user()       → Register a new user (returns True/False)
  - login_user()        → Verify credentials (returns True/False)
  - save_history()      → Save a match result for a user
  - get_user_history()  → Retrieve all match history for a user
  - delete_history()    → Delete a specific history record

Author: AI Resume–JD Matcher (MCA Major Project)
"""

import sqlite3
import hashlib
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

# ---------------------------------------------------------------------------
# Database path — relative to this file's location (src/ → data/)
# ---------------------------------------------------------------------------
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH   = os.path.join(_BASE_DIR, "data", "app_database.db")


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _get_connection() -> sqlite3.Connection:
    """
    Open and return a SQLite connection with row_factory set to
    sqlite3.Row (enables dict-like column access on result rows).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")   # better concurrency
    return conn


def _hash_password(password: str) -> str:
    """
    Hash a plain-text password using SHA-256.

    Args:
        password (str): Plain-text password.

    Returns:
        str: Hex-encoded SHA-256 digest.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 1. init_db()  — Create tables if they don't exist
# ---------------------------------------------------------------------------

def init_db() -> None:
    """
    Initialize the SQLite database and create required tables.

    Tables created (if not already present):
      - users   : stores registered user credentials.
      - history : stores resume-JD match results per user.

    Should be called once at application startup.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with _get_connection() as conn:
        conn.executescript("""
            -- Users table
            CREATE TABLE IF NOT EXISTS users (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT    NOT NULL UNIQUE,
                password  TEXT    NOT NULL,
                created_at TEXT   DEFAULT (datetime('now'))
            );

            -- Match history table
            CREATE TABLE IF NOT EXISTS history (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                username       TEXT    NOT NULL,
                resume_name    TEXT    NOT NULL,
                jd_name        TEXT    DEFAULT 'N/A',
                match_score    REAL    NOT NULL,
                matched_skills TEXT    DEFAULT '',
                missing_skills TEXT    DEFAULT '',
                extra_skills   TEXT    DEFAULT '',
                timestamp      TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (username) REFERENCES users(username)
            );
        """)
    print(f"[database] Initialized DB at: {DB_PATH}")


# ---------------------------------------------------------------------------
# 2. create_user()  — Register a new user
# ---------------------------------------------------------------------------

def create_user(username: str, password: str) -> Dict[str, Any]:
    """
    Register a new user in the users table.

    Passwords are stored as SHA-256 hashes — never in plain text.

    Args:
        username (str): Desired username (must be unique).
        password (str): Plain-text password (will be hashed).

    Returns:
        dict: {
            "success" : bool,
            "message" : str   — human-readable result,
        }
    """
    if not username.strip() or not password.strip():
        return {"success": False, "message": "Username and password cannot be empty."}

    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}

    hashed = _hash_password(password)

    try:
        with _get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username.strip(), hashed),
            )
        return {"success": True, "message": f"User '{username}' registered successfully!"}

    except sqlite3.IntegrityError:
        return {"success": False, "message": f"Username '{username}' is already taken."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {e}"}


# ---------------------------------------------------------------------------
# 3. login_user()  — Verify credentials
# ---------------------------------------------------------------------------

def login_user(username: str, password: str) -> Dict[str, Any]:
    """
    Verify a user's login credentials.

    Args:
        username (str): Username to look up.
        password (str): Plain-text password to verify.

    Returns:
        dict: {
            "success"  : bool,
            "message"  : str,
            "username" : str | None — set on success,
        }
    """
    if not username.strip() or not password.strip():
        return {"success": False, "message": "Username and password are required.",
                "username": None}

    hashed = _hash_password(password)

    try:
        with _get_connection() as conn:
            row = conn.execute(
                "SELECT username FROM users WHERE username = ? AND password = ?",
                (username.strip(), hashed),
            ).fetchone()

        if row:
            return {"success": True,
                    "message": f"Welcome back, {username}!",
                    "username": username.strip()}
        else:
            return {"success": False,
                    "message": "Invalid username or password.",
                    "username": None}

    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {e}", "username": None}


# ---------------------------------------------------------------------------
# 4. save_history()  — Persist a match result
# ---------------------------------------------------------------------------

def save_history(
    username       : str,
    resume_name    : str,
    match_score    : float,
    missing_skills : List[str],
    jd_name        : str        = "N/A",
    matched_skills : List[str]  = None,
    extra_skills   : List[str]  = None,
) -> Dict[str, Any]:
    """
    Save a resume–JD match result to the history table.

    Skill lists are stored as comma-separated strings for simplicity.

    Args:
        username       (str):        Logged-in username.
        resume_name    (str):        Filename of the uploaded resume.
        match_score    (float):      Cosine similarity score (0–100).
        missing_skills (List[str]):  Skills from JD absent in resume.
        jd_name        (str):        Name/label of the job description.
        matched_skills (List[str]):  Skills present in both (optional).
        extra_skills   (List[str]):  Resume skills not in JD (optional).

    Returns:
        dict: { "success": bool, "message": str }
    """
    def _join(skills):
        return ", ".join(sorted(skills)) if skills else ""

    try:
        with _get_connection() as conn:
            conn.execute(
                """INSERT INTO history
                   (username, resume_name, jd_name, match_score,
                    matched_skills, missing_skills, extra_skills, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    username,
                    resume_name,
                    jd_name,
                    round(float(match_score), 2),
                    _join(matched_skills),
                    _join(missing_skills),
                    _join(extra_skills),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
        return {"success": True, "message": "Match history saved."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {e}"}


# ---------------------------------------------------------------------------
# 5. get_user_history()  — Retrieve a user's match history
# ---------------------------------------------------------------------------

def get_user_history(username: str) -> List[Dict[str, Any]]:
    """
    Retrieve all match history records for a given user,
    sorted by newest first.

    Args:
        username (str): The logged-in username.

    Returns:
        List[dict]: Each dict contains keys matching the history columns.
                    Returns an empty list if no records exist.
    """
    try:
        with _get_connection() as conn:
            rows = conn.execute(
                """SELECT id, resume_name, jd_name, match_score,
                          matched_skills, missing_skills, extra_skills, timestamp
                   FROM    history
                   WHERE   username = ?
                   ORDER BY timestamp DESC""",
                (username,),
            ).fetchall()

        return [dict(row) for row in rows]

    except sqlite3.Error as e:
        print(f"[database] get_user_history error: {e}")
        return []


# ---------------------------------------------------------------------------
# 6. delete_history()  — Remove a specific history record
# ---------------------------------------------------------------------------

def delete_history(record_id: int, username: str) -> Dict[str, Any]:
    """
    Delete a single history record by its ID.
    The username is checked to prevent cross-user deletion.

    Args:
        record_id (int): Primary key of the history record.
        username  (str): Must match the record's owner.

    Returns:
        dict: { "success": bool, "message": str }
    """
    try:
        with _get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM history WHERE id = ? AND username = ?",
                (record_id, username),
            )
        if cursor.rowcount > 0:
            return {"success": True,  "message": "Record deleted."}
        else:
            return {"success": False, "message": "Record not found or access denied."}

    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {e}"}


# ---------------------------------------------------------------------------
# 7. create_user_db()  — Low-level insert used by auth.py
# ---------------------------------------------------------------------------

def create_user_db(username: str, hashed_password: str) -> bool:
    """
    Insert a new user row with a pre-hashed password.

    Called by ``src.auth.register_user()`` after hashing is done there.
    Returns True on success, False if the username already exists or on
    any other database error.

    Args:
        username        (str): Unique username.
        hashed_password (str): SHA-256 hex digest of the plain-text password.

    Returns:
        bool: True if the row was inserted, False otherwise.
    """
    try:
        with _get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username.strip(), hashed_password),
            )
        return True
    except sqlite3.IntegrityError:
        return False  # username already taken
    except sqlite3.Error:
        return False


# ---------------------------------------------------------------------------
# 8. get_user_db()  — Retrieve stored hash for a username (used by auth.py)
# ---------------------------------------------------------------------------

def get_user_db(username: str) -> Optional[str]:
    """
    Fetch the stored password hash for a given username.

    Called by ``src.auth.authenticate_user()`` to retrieve the hash so
    it can be compared against the freshly-hashed login attempt.

    Args:
        username (str): Username to look up.

    Returns:
        str  — stored hash if the user exists.
        None — if the username does not exist or a DB error occurs.
    """
    try:
        with _get_connection() as conn:
            row = conn.execute(
                "SELECT password FROM users WHERE username = ?",
                (username.strip(),),
            ).fetchone()
        return row["password"] if row else None
    except sqlite3.Error:
        return None


# ---------------------------------------------------------------------------
# Quick self-test (run directly: python src/database.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== database.py — Self-Test ===\n")

    # 1. Initialize
    init_db()

    # 2. Register users
    print(create_user("alice", "secure123"))
    print(create_user("alice", "secure123"))   # duplicate — should fail
    print(create_user("bob",   "pass456"))

    # 3. Login
    print(login_user("alice", "secure123"))    # should succeed
    print(login_user("alice", "wrong"))        # should fail

    # 4. Save history
    print(save_history(
        username       = "alice",
        resume_name    = "alice_resume.pdf",
        match_score    = 78.5,
        missing_skills = ["aws", "kubernetes"],
        jd_name        = "jd_data_scientist.txt",
        matched_skills = ["python", "machine learning", "sql"],
        extra_skills   = ["django"],
    ))

    # 5. Fetch history
    records = get_user_history("alice")
    print(f"\nHistory for alice ({len(records)} record(s)):")
    for rec in records:
        print(f"  [{rec['id']}] {rec['resume_name']} | Score: {rec['match_score']}%"
              f" | {rec['timestamp']}")

    # 6. Delete
    if records:
        print(delete_history(records[0]["id"], "alice"))

    print("\n=== Self-test complete ===")
