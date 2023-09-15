#!/usr/bin/env python3
""" Auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


class Auth:
    """Auth class to interact with authentication database
    """
    def __init__(self):
        """Initialize Auth class instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        Args:
            email (str): user's email address
            hashed_password (str): user's password hashed by bcrypt's hashpw
        Return:
            (User): Newly created User class instance
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            new_user = self._db.add_user(email, password)
            return new_user
        else:
            raise ValueError(f'User {email} already exists')


def _hash_password(password: str) -> bytes:
    """Hash password input
    Args:
        password (str): user password
    Return:
        (bytes): salted hash of input password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
