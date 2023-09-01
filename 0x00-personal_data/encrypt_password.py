#!/usr/bin/env python3
"""Password Encryption Module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password and return byte string"""
    password = str.encode(password)
    hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pwd
