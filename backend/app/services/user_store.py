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
            role          TEXT NOT NULL DEFAULT 'user',
            status        TEXT NOT NULL DEFAULT 'active',
            last_session  TIMESTAMP,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Idempotent column additions for older schemas
    for col, defn in [
        ('role',         "TEXT NOT NULL DEFAULT 'user'"),
        ('status',       "TEXT NOT NULL DEFAULT 'active'"),
        ('last_session', 'TIMESTAMP'),
    ]:
        try:
            conn.execute(f'ALTER TABLE users ADD COLUMN {col} {defn}')
        except sqlite3.OperationalError:
            pass
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


def get_user_role(email: str) -> str:
    """Return the role string for a user, defaulting to 'user'."""
    normalized = email.lower().strip()
    with _connect() as conn:
        row = conn.execute(
            'SELECT role FROM users WHERE email = ?', (normalized,)
        ).fetchone()
    return row[0] if row else 'user'


def set_user_role(email: str, role: str) -> bool:
    """Promote / demote a user's role. Returns True on success."""
    normalized = email.lower().strip()
    with _connect() as conn:
        cur = conn.execute(
            'UPDATE users SET role = ? WHERE email = ?', (role, normalized)
        )
    return cur.rowcount > 0


def update_last_session(email: str):
    """Stamp the last_session timestamp for a user."""
    import datetime
    normalized = email.lower().strip()
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    conn = _connect()
    try:
        conn.execute('UPDATE users SET last_session = ? WHERE email = ?', (now, normalized))
        conn.commit()
    finally:
        conn.close()