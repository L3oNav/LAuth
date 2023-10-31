from app.users.models import User, Account
from app.settings.database import get_session
from app.settings import get_settings
from fastapi import Depends, Request, HTTPException, Security, status
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import ValidationError
from jose import jwt
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
        token = self._create_access_token(user, data['access_token'])
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

    def is_token_expired(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            expiration_time = payload.get("exp")
            if expiration_time is None:
                return False
            current_time = datetime.utcnow().timestamp()
            return current_time > expiration_time
        except Exception as e:
            return True

    async def refresh_access_token(self, access_token, refresh_token):

        access_payload = jwt.decode(access_token, get_settings().SECRET_KEY, algorithm="HS256")
        refresh_payload = jwt.decode(refresh_token, get_settings().SECRET_KEY, algorithm="HS256")

        user_id = refresh_payload.get("sub")
        email = access_payload.get("sub")

        user = get_user({ "user_id": user_id, "email": email }, w_acc = False )

        if (user_id is None) or (email is None) or (user is None):
            raise HTTPException("access_token and refresh_token don't match", status.HTTP_417_EXPECTATION_FAILED)

        return self._create_access_token(data={"email": email, "user_id": user_id})

    def get_user(self, data, w_acc = True) -> dict:
        session = self.session
        session = next(session())
        if w_acc:
            return session.query(User).filter(User.accounts.any(Account.issuer == data['iss']), User.email == data['email']).first()
        else:
            return session.query(User).filter(User.id == data['user_id'], User.email == data['email']).first()

    def _create_access_token(self, data: dict, access_token: str) -> dict:
        """

        """
        to_encode = data

        expire_access_token = datetime.utcnow() + timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRATION_MINUTES)
        expire_refresh_token = datetime.utcnow() + timedelta(minutes=get_settings().REFRESH_TOKEN_EXPIRATION_MINUTES)

        access_token_payload = {
            "exp": expire_access_token,
            "sub": data.email,
        }

        refresh_token_payload = {
            "exp": expire_refresh_token,
            "sub": str(data.id),
        }

        access_token = jwt.encode(access_token_payload, get_settings().SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(refresh_token_payload, get_settings().SECRET_KEY, algorithm="HS256")

        self._set_session_data(f"user:{to_encode.email.lower()}:access_token", access_token)
        self._set_session_data(f"user:{to_encode.email.lower()}:refresh_token", refresh_token)

        return {"access_token": access_token, "refresh_token": access_token, "user": to_encode.email}

user_manager = UserManager()
