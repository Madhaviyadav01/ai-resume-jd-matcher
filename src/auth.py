from __future__ import annotations

import hashlib

from src.database import create_user_db, get_user_db


# ---------------------------------------------------------------------------
# 1. hash_password()
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using SHA-256.

    Args:
        password (str): The raw password string to hash.

    Returns:
        str: Hex-encoded SHA-256 digest (64 characters).

    Example:
        >>> hash_password("mySecret1")
        'e9c4....'  # 64-char hex string
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 2. register_user()
# ---------------------------------------------------------------------------

def register_user(username: str, password: str) -> bool:
    """
    Register a new user by hashing the password and persisting to the DB.

    Steps:
        1. Hash the password with SHA-256 via ``hash_password()``.
        2. Call ``create_user_db(username, hashed_password)`` to insert the
           row into the ``users`` table.

    Args:
        username (str): Desired username (must be unique).
        password (str): Plain-text password chosen by the user.

    Returns:
        bool: True if registration succeeded, False if the username is
              already taken or any database error occurred.
    """
    if not username.strip() or not password.strip():
        return False

    hashed = hash_password(password)
    return create_user_db(username.strip(), hashed)


# ---------------------------------------------------------------------------
# 3. authenticate_user()
# ---------------------------------------------------------------------------

def authenticate_user(username: str, password: str) -> bool:
    """
    Verify a user's credentials against the stored SHA-256 hash.

    Steps:
        1. Retrieve the stored hash via ``get_user_db(username)``.
        2. Hash the supplied password with ``hash_password()``.
        3. Compare the two hashes and return the result.

    Args:
        username (str): Username to look up.
        password (str): Plain-text password to verify.

    Returns:
        bool: True if credentials are valid, False otherwise
              (including unknown username or DB errors).
    """
    if not username.strip() or not password.strip():
        return False

    stored_hash = get_user_db(username.strip())

    # Unknown username — get_user_db returns None
    if stored_hash is None:
        return False

    return hash_password(password) == stored_hash
