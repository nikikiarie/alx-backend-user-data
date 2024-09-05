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
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        if not user_id or not isinstance(user_id, str):
            return
        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id
