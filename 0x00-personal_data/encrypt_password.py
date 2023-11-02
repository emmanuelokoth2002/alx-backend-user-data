#!/usr/bin/env python3
"""
Hashing and Salting Passwords
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes and salts the provided password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: A salted, hashed password.
    """

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates whether the provided password matches the given hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to verify against the hashed password.

    Returns:
        bool: True if the password matches the hashed password,False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
