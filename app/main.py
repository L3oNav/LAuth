from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette_authlib.middleware import AuthlibMiddleware as SessionMiddleware
from app.auth.urls import google_router
from app.settings import get_settings
from app.auth.oauth import oauth
import os

app = FastAPI()

print(get_settings().SECRET_KEY)

app.add_middleware(
    SessionMiddleware, 
    secret_key  = get_settings().SECRET_KEY,
    max_age = 60 * get_settings().ACCESS_TOKEN_EXPIRATION_MINUTES,
    session_cookie = "session_id"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:3000",
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google_router)
@app.get("/")
async def main(request: Request):
    urls = [{"path": route.path, "name": route.name} for route in request.app.routes]
    print(request.session)
    return {
        "secrert_key": [get_settings().SECRET_KEY if get_settings().ENVIROMENT == "development" else "*************"],
        "session": [request.session if get_settings().ENVIROMENT == "development" else "*************"],
        "message": "Hello World",
        "env": os.getenv("ENVIROMENT", "development"),
        "urls": urls
    }

@app.get("/logout")
async def logout(request: Request):
    request.session['sessionId'] = None
    return {"message": "Logout success"}
