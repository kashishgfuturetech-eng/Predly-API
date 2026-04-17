"""
Simple SQLite-backed user store for credential-based login.
Uses werkzeug (Flask dependency) for password hashing.
"""

import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

_DB_PATH = os.path.join(os.path.dirname(__file__), '../../uploads/users.db')


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT UNIQUE NOT NULL,
            passkey_hash  TEXT NOT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn


def create_user(email: str, passkey: str) -> tuple[bool, str]:
    """
    Create a new user. Returns (True, '') on success or (False, reason) on failure.
    """
    normalized = email.lower().strip()
    try:
        with _connect() as conn:
            conn.execute(
                'INSERT INTO users (email, passkey_hash) VALUES (?, ?)',
                (normalized, generate_password_hash(passkey)),
            )
        return True, ''
    except sqlite3.IntegrityError:
        return False, 'An account with that email already exists.'


def verify_user(email: str, passkey: str) -> bool:
    """Return True if the email/passkey pair is valid."""
    normalized = email.lower().strip()
    with _connect() as conn:
        row = conn.execute(
            'SELECT passkey_hash FROM users WHERE email = ?', (normalized,)
        ).fetchone()
    if not row:
        return False
    return check_password_hash(row[0], passkey)


def email_exists(email: str) -> bool:
    normalized = email.lower().strip()
    with _connect() as conn:
        row = conn.execute(
            'SELECT 1 FROM users WHERE email = ?', (normalized,)
        ).fetchone()
    return row is not None
