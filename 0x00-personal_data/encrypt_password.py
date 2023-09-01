#!/usr/bin/env python3
"""Password Encryption Module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password and return byte string"""
    password = str.encode(password)
    hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str):
    """Validate hashed password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
