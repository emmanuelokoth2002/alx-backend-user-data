#!/usr/bin/env python3
'''
Module for User Authentication
'''
from flask import request
from typing import List, TypeVar
import os


class Auth:
    ''' Class handling authentication '''

    def require_auth(self, requested_path: str,
                     exclude_list: List[str]) -> bool:
        ''' Check if authentication is required '''
        if requested_path is None:
            return True
        if exclude_list is None or exclude_list == []:
            return True
        if requested_path in exclude_list:
            return False

        for excluded_path in exclude_list:
            if excluded_path.startswith(requested_path):
                return False
            elif requested_path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == '*':
                if requested_path.startswith(excluded_path[:-1]):
                    return False
        return True

    def authorization_header(self, req=None) -> str:
        ''' Get the authorization header '''
        if req is None:
            return None
        auth_header = req.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, req=None) -> TypeVar('User'):
        ''' Fetch the current user '''
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.

        Args:
            request: Flask request object.

        Returns:
            Cookie value from the request's cookies dictionary.
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
