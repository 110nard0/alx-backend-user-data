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
        slashed_path = f'{path}/' if path and not path.endswith('/') else path
        if not path or not excluded_paths:
            return True
        elif path not in excluded_paths and slashed_path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Validates requests to secure API
        """
        if request and request.headers.get('Authorization'):
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Authenticates current user for request
        """
        return request
