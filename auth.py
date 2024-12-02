"""Authentication management."""

import hashlib
import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class User:
    username: str
    password_hash: str

class AuthManager:
    def __init__(self):
        self._users = self._load_users()

    def _load_users(self) -> dict:
        # In production, this should load from a secure database
        return {
            "admin": User(
                username="admin",
                password_hash=self._hash_password("admin")  # Don't use hardcoded passwords in production
            )
        }

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using SHA-256 with salt."""
        salt = os.urandom(32)
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        ).hex()

    def validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials."""
        user = self._users.get(username)
        if not user:
            return False
        return self._hash_password(password) == user.password_hash