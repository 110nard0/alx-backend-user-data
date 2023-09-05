#!/usr/bin/env python3
"""
Auth class module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class manages Simple API Authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Confirms path route in list of excluded paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Validates requests to secure API
        """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """Authenticates current user for request
        """
        return request
