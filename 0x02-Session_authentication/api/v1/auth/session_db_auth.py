#!/usr/bin/env python3
"""
SessionDBAuth class module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class inherits from SessionExpAuth class and implements
    an authentication system, based on Session IDs stored in a database
    """
    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a User ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        uid = super().user_id_for_session_id(session_id)
        if uid is None:
            if UserSession.search({'session_id': session_id}):
                pass
            else:
                return None
        if not UserSession.all():
            return None
        sessions = UserSession.search({'session_id': session_id})
        if sessions:
            session = sessions[0]
            return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy a valid UserSession based on Session ID in request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        sessions = UserSession.search({'session_id': session_id})
        if sessions:
            sessions[0].remove()
            return True
        return False
