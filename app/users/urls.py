from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from authlib.integrations.starlette_client import OAuthError
from app.auth.oauth import oauth
from app.users import user_manager
import secrets

google_router = APIRouter(prefix="/v1/auth/google")

@google_router.get('/login')
async def login_via_google(request: Request):
    redirect_uri = request.url_for('authorize_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@google_router.get('/auth')
async def authorize_google(request: Request):
    try:
        user_info = await oauth.google.authorize_access_token(request)
    except OAuthError as err:
        print(err)
        return err.error
    token = user_manager.authenticate_w_google(data=user_info)
    if not token:
        raise HTTPException(status_code=400, detail="Token is not returned")
    return token 
