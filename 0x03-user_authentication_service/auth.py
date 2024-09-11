#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Password hashing
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ returns a uuid4 str """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Initializes Auth object
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ checks if user details are calid"""
        try:
            user = self._db.find_user_by(email=email)
            by = bytes(password, 'utf-8')
            if bcrypt.checkpw(by, user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ creates a new session for user with email """
        try:
            user = self._db.find_user_by(email=email)
            id_session = _generate_uuid()
            self._db.update_user(user.id, session_id=id_session)
            return id_session
        except Exception:
            pass

     def get_user_from_session_id(self, session_id: str) -> User:
        """ gets user from session_id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None
