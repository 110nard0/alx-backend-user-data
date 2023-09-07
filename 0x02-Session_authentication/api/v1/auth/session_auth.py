#!/usr/bin/env python3
"""
SessionAuth class module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth class inherits from Auth class and implements the
    WWW Session Authentication scheme
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a User ID
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Return a User instance based on a cookie value
        """
        if request is None:
            return None
        cookie = self.session_cookie(request)
        if cookie is None:
            return None
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)
