#!/usr/bin/env python3
"""
BasicAuth class module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """BasicAuth class inherit from Auth class and implements the
    WWW Basic Authentication scheme
    """
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """Returns the Base64 part of the Authorization header
        """
        if authorization_header is None\
                or type(authorization_header) is not str\
                or not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Returns decoded value of a Base64 string base64_authorization_header
        """
        if base64_authorization_header is None\
                or type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                          base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Return the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None\
                or type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' in decoded_base64_authorization_header:
            return tuple(decoded_base64_authorization_header.split(':', 1))
        else:
            return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        for user in User.search():
            if user.email == user_email and user.is_valid_password(user_pwd):
                return user
        return None
