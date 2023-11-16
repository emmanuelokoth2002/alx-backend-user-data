#!/usr/bin/env python3
"""
Auth module
"""

from db import DB
from user import User
import bcrypt


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            User: The newly created User object.
        """
        existing_user = self._db.find_user_by_email(email)

        if existing_user:
            raise ValueError(f'User {email} already exists')
        hashed_password = self._hash_password(password)

        new_user = self._db.add_user(email, hashed_password)

        return new_user

    def _hash_password(password: str) -> bytes:
        """
        Hashes a password using bcrypt.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The salted hash of the input password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password
