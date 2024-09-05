#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, TypeVar
from models.user import User
import os


class Auth:
    """ Auth class """

    def require_auth(
        self, path: str, excluded_paths: List[str]
    ) -> bool:
        """ determines if authentication is required """
        if path and not path.endswith('/'):
            path = path + '/'
        for e_path in excluded_paths:
            if path.startswith(e_path.split('*')[0]):
                return False
        if not path or path not in excluded_paths:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        return False

    def authorization_header(self, request=None) -> str:
        """
        Checks auth header
        """
        key = 'Authorization'

        if request is None or key not in request.headers:
            return
        return request.headers.get(key)

    def current_user(self, request=None) -> None:
        """
        doc str
        """
        return

    def session_cookie(self, request=None):
        """ gets session cookie """
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
