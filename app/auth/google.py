from fastapi import APIRouter
from starlette.requests import Request
from app.auth.oauth import oauth

google_router = APIRouter(prefix="/v1/auth/google")

@google_router.get('/login')
async def login_via_google(request: Request):
    redirect_uri = request.url_for('authorize_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@google_router.get('/auth')
async def authorize_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token
    return dict(user)
