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
        
        for session_id, stored_user_id in self.user_id_by_session_id.items():
            if stored_user_id == user_id:
                return session_id
        
        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        if not session_id or not isinstance(session_id, str):
            return
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id
