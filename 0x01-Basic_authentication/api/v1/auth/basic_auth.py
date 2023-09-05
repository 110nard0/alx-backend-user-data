#!/usr/bin/env python3
"""
BasicAuth class module for the API
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class inherit from Auth class and implements the
    Basic HTTP Authentication scheme
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None or type(authorization_header)\
                is not str or not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ', 1)[1]
