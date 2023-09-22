from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.auth.urls import google_router
from app.settings import get_settings
import os

app = FastAPI()

SK = get_settings().SECRET_KEY

app.add_middleware(SessionMiddleware, secret_key=SK)
app.add_middleware(
    CORSMiddleware,
    allow_origins= [ "http://localhost:8000", "http://localhost" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google_router)

@app.get("/")
async def main(request: Request):
    user = [dict(request.session['user']) if request.session.get('user') else None]
    urls = [{"path": route.path, "name": route.name} for route in request.app.routes]
    return {
        "user": user,
        "secrert_key": [SK if get_settings().ENVIROMENT == "development" else "*************"],
        "message": "Hello World",
        "env": os.getenv("ENVIROMENT", "development"),
        "urls": urls
    }

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return {"message": "Logout success"}
