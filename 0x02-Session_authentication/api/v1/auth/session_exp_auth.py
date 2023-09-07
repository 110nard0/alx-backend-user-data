#!/usr/bin/env python3
"""
SessionExpAuth class module for the API
"""
from api.v1.auth.session_auth import SessionAuth
from models.user import User

from datetime import datetime, timedelta
from os import getenv
from typing import TypeVar
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class inherits from SessionAuth class and implements the
    WWW Session Authentication scheme with expiration
    """
    def __init__(self):
        """Instantiate new SessionExpAuth class instance
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a User ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if not self.user_id_by_session_id.get(session_id):
            return None

        session_dictionary = self.user_id_by_session_id[session_id]
        user_id = session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')

        if self.session_duration <= 0:
            return user_id
        if not created_at:
            return None

        current_datetime = datetime.now()
        expiry = created_at + timedelta(seconds=self.session_duration)
        if expiry < current_datetime:
            return None

        return user_id
