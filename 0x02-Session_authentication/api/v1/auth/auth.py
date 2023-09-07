#!/usr/bin/env python3
"""
Auth class module for the API
"""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """Auth class manages Simple API Authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Confirm path route in list of excluded paths
        """
        slashed_path = f'{path}/' if path and not path.endswith('/') else path

        if not path or not excluded_paths:
            return True
        for route in excluded_paths:
            if route.endswith('*') and path.startswith(route[:-1]):
                return False
        if path not in excluded_paths and slashed_path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Validate requests to secure API using Auhtorization Header
        """
        if request and request.headers.get('Authorization'):
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Authenticate current user sending request
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Return a cookie value from a request
        """
        if request is None:
            return None
        SESSION_NAME = getenv("SESSION_NAME")
        return request.cookies.get(SESSION_NAME)
