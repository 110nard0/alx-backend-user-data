#!/usr/bin/env python3
"""
BasicAuth class module for the API
"""
from api.v1.auth.auth import Auth
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
            return base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None
