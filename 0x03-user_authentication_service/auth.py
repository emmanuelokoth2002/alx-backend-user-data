#!/usr/bin/env python3
'''
User Authentication Module
'''

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid
from typing import Union

def hash_password(password: str) -> bytes:
    ''' Hashes a password using bcrypt. '''
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd

def generate_uuid() -> str:
    ''' Generates a UUID. '''
    return str(uuid.uuid4())

class Auth:
    ''' Auth class for user authentication. '''

    def __init__(self):
        ''' Initializes an instance of Auth. '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[User, None]:
        ''' Registers a new user. '''
        if not email or not password:
            return None
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
        except NoResultFound:
            # If user does not exist, add to the database
            return self._db.add_user(email, hash_password(password))
        else:
            # If user already exists, raise an error
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        ''' Validates user credentials for login. '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        ''' Creates a user session. '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            session_id = generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        ''' Finds a user by session id. '''
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        ''' Destroys a user session. '''
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> Union[str, None]:
        ''' Generates a reset password token. '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError('User not found')
        else:
            pwd_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=pwd_token)
            return pwd_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        ''' Updates user password using reset token. '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError('Invalid reset token')
        else:
            user.hashed_password = hash_password(new_password)
            user.reset_token = None
            return None
