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
            new_user = self._db.add_user(email, _hash_password(password))
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
            if bcrypt.checkpw(password.encode(),
                              user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create session for current user
        Args:
            email (str): returning user's email address
        Return:
            session_id (str): unique string associated with particular user
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(session_id: str) -> User:
        """Fetch user using Session ID
        Args:
            session_id (str): unique string associated with particular user
        Return:
            (User) object with session_id attribute (SUCCESS) or None (FAIL)
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        else:
            return user

    def destroy_session(user_id: int) -> None:
        """Destroys user session
        Args:
            user_id (int): unique auto-generated database User ID
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except Exception:
            return None
        else:
            user.session_id = None


def _generate_uuid() -> str:
    """Generate string representation of UUID
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
