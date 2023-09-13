#!/usr/bin/env python3
""" Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hash password input
    Args:
        password (str): user password
    Return:
        (bytes): salted hash of input password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
