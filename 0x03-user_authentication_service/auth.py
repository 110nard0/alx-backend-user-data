#!/usr/bin/env python3
""" Auth module
"""
import bcrypt
import uuid
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
            email (str): new user's email address
            password (str): new user's password
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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user's login
        Args:
            email (str): returning user's email address
            password (str): returning user's password
        Return:
            (bool): True if valid password for email else False
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(user.hashed_password.encode(),
                              _hash_password(password)):
                return True
            return False
        except NoResultFound:
            return False


def _generate_uuid() -> str:
    """Generate string represntation of UUID
    Return:
        (str): uuid object represented as a string
    """
    return str(uuid.uuid4())

def _hash_password(password: str) -> bytes:
    """Hash password input
    Args:
        password (str): user password
    Return:
        (bytes): salted hash of input password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())