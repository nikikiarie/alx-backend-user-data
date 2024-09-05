#!/usr/bin/env python3
"""
SessionAuth class
"""
from flask import abort, request
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class """
    user_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        if not isinstance(user_id, str) or not user_id:
            return
        session_id = str(uuid4())

        self.user_session_id[session_id] = user_id

        return session_id
