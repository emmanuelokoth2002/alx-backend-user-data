#!/usr/bin/env python3
'''
Module for Basic Authentication
'''
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User

class BasicAuth(Auth):
    ''' Class handling Basic Authentication '''

    def extract_base64_authorization_header(self,
                                           auth_header: str) -> str:
        ''' Extracts the Base64 part from Authorization header '''
        if auth_header is None:
            return None
        if not isinstance(auth_header, str):
            return None
        if not auth_header.startswith('Basic '):
            return None
        token = auth_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(
            self, base64_header: str) -> str:
        ''' Decodes Base64 '''
        if base64_header is None:
            return None
        if not isinstance(base64_header, str):
            return None
        try:
            decoded_value = base64.b64decode(base64_header)
            return decoded_value.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_header: str) -> (str, str):
        ''' Extracts user credentials '''
        if decoded_base64_header is None:
            return (None, None)
        if not isinstance(decoded_base64_header, str):
            return (None, None)
        if ':' not in decoded_base64_header:
            return (None, None)
        email, password = decoded_base64_header.split(':')
        return (email, password)

    def user_object_from_credentials(
            self, email: str, pwd: str) -> TypeVar('User'):
        ''' Generates User object '''
        if email is None or not isinstance(email, str):
            return None
        if pwd is None or not isinstance(pwd, str):
            return None
        try:
            users = User.search({'email': email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, req=None) -> TypeVar('User'):
        ''' Overloaded current_user method for Basic Authentication '''
        auth_header = self.authorization_header(req)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        credentials = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(*credentials)
