#!/usr/bin/env python3
"""
SessionAuth class module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """SessionAuth class inherits from Auth class and implements the
    WWW Session Authentication scheme
    """
    pass
