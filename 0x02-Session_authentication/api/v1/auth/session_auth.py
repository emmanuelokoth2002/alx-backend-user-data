#!/usr/bin/env python3
"""
Module: session_auth
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session Authentication Class.

    This class manages session authentication and provides methods to create
    session IDs.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id: User ID for whom the session ID needs to be created.

        Returns:
            Session ID if user_id is a string, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value."""
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)

        if user_id is None:
            return None

        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Deletes the user session / logout."""
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)

        if not session_cookie or not user_id:
            return False

        del self.user_id_by_session_id[session_cookie]
        return True
