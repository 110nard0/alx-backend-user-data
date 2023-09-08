#!/usr/bin/env python3
"""session db auth module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import os


class SessionDBAuth(SessionExpAuth):
    """Session DB auth class"""

    def create_session(self, user_id: str = None) -> str:
        """create the session"""
        session_id = super().create_session(user_id)

        session_model = UserSession()
        session_model.user_id = user_id
        session_model.session_id = session_id
        session_model.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """get the user id for session"""
        if session_id is None:
            print("no session id")
            return None

        UserSession.load_from_file()

        user = UserSession.search({"session_id": session_id})

        if not user or len(user) == 0:
            return None
        user = user[0]
        return user.user_id

    def destroy_session(self, request=None):
        """destroy the db session"""
        if request is None:
            return False
        if not self.session_cookie(request):
            return False

        if not self.user_id_for_session_id(self.session_cookie(request)):
            return False

        session_id = self.session_cookie(request)

        print("session_Id", session_id)

        user = UserSession.search({"session_id": session_id})

        print("user", user)
        if not user or len(user) == 0:
            return None

        user = user[0]

        user.remove()
