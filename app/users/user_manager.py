from app.users.models import User, Account
from app.settings.database import get_session
from app.settings import get_settings
from fastapi import Depends, Request, HTTPException, Security, status
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import ValidationError
from authlib.jose import jwt
from app.auth.oauth import oauth
from app.settings.redis import get_redis_connection
import asyncio

class UserManager:

    def __init__(self):
        self.session = get_session
        self.oauth = oauth
        self.redis = get_redis_connection()

    def _set_session_data(self, key, value):
        self.redis.set(key, value)
        return self.redis.get(key)

    def _get_session_data(self, key):
        return self.redis.get(key)

    def delete_session_data(self, key):
        try:
            self.redis.delete(key)
            return True
        except Exception as e:
            return False

    def authenticate_w_google(self, data):
        user_info = data['userinfo']
        user = self._get_or_create_user(user_info)
        token = self._create_access_token({"sub":f"{user_info.email.lower()}", "scopes": ['me']}, data['access_token'])
        return token 

    def _create_account(self, data: dict, user):
        session = self.session
        session = next(session())
        exist_account = session.query(Account).filter_by(issuer=data['iss'], subject=data['sub']).first()
        if exist_account:
            return None
        new_account = Account(
            issuer=data['iss'],
            subject=data['sub'],
            user=user
        )
        return new_account

    def _get_or_create_user(self, data):
        user = self.get_user(data)
        if not user:
            user = self._create_user(data)
        return user

    def _create_user(self, data):
        session = self.session
        session = next(session())
        exist_user = session.query(User).filter_by(email=data['email']).first()
        if exist_user:
            raise Exeption("User already exist")
        new_user = User(
            email=data['email'],
        )
        new_account = self._create_account(
            data=data,
            user=new_user
        )
        session.add(new_user)
        session.add(new_account)
        session.commit()
        session.close()
        return new_user 

    def refresh_google_token():
        pass

    def get_user(self, data):
        try:
            session = self.session
            session = next(session())
            return session.query(User).filter(User.accounts.any(Account.issuer == data['iss']), User.email == data['email']).first()
        except Exception as e:
            print(data.keys())
            raise e

    def _create_access_token(self, data: dict, access_token: str) -> dict:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRATION_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, get_settings().SECRET_KEY, algorithm="HS256")
        self._set_session_data(f"user:{data['sub']}:access_token", access_token)
        return {"authorization_token": encoded_jwt, "email": data['sub']}
        
user_manager = UserManager()
