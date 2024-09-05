#!/usr/bin/env python3
"""Handle basic auth"""
import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Defines attributes and methods for basic authorization
    Inherits from Auth
    Args:
        Auth (class): Parent authentication class
    """

    def extract_base64_authorization_header(self, authorization_header):
        """Returns the Base64 part of the Authorization header
        Args:
            authorization_header (str): auth_header
        Returns:
            str: base64 part of header
        """
        if not (authorization_header and isinstance(authorization_header, str)
                and authorization_header.startswith('Basic ')):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header):
        """Returns the decoded value of a Base64 string
        Args:
            base64_authorization_header (str): base64 auth header
        Returns:
            str: decoded value of base64 string
        """
        if not (base64_authorization_header and
                isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header):
        """Extracts user email and password from the Base64 decoded value.
        Args:
            decoded_base64_authorization_header (str): auth header
        Returns:
            tuple: (str, str) user email and password
        """
        if not (decoded_base64_authorization_header and
                isinstance(decoded_base64_authorization_header, str) and
                ':' in decoded_base64_authorization_header):
            return None, None

        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email, user_pwd):
        """Returns the User instance based on email and password.
        Args:
            user_email (str): user email
            user_pwd (str): user password
        Returns:
            User or None: User instance if valid credentials are found
            else None
        """
        if not (user_email and isinstance(user_email, str) and
                user_pwd and isinstance(user_pwd, str)):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None):
        """Gets current user"""
        try:
            auth_header = self.authorization_header(request)
            encoded = self.extract_base64_authorization_header(auth_header)
            decoded = self.decode_base64_authorization_header(encoded)
            email, password = self.extract_user_credentials(decoded)
            return self.user_object_from_credentials(email, password)
        except Exception:
            return None
