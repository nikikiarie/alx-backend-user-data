#!/usr/bin/env python3
"""
SessionAuth class
"""
from flask import abort, request
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class """
    pass
