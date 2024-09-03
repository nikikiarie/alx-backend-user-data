#!/usr/bin/env python3


from flask import request, Flask
from typing import List, TypeVar


class Auth:
    ''' A Class to manage the API authentication.
    '''

    def require_auth(
            self,
            path: str,
            excluded_paths: List[str]
            ) -> bool:
        ''' Required auth
        '''
        return False

    def authorization_header(
            self,
            request=None
            ) -> str:
        '''Auth header
        '''
        request = Flask(__name__)
        return None

    def current_user(
            self,
            request=None
            ) -> TypeVar('User'):
        ''' Current User
        '''
        request = Flask(__name__)
        return None