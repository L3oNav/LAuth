from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.auth.oauth import oauth

google_router = APIRouter(prefix="/v1/auth/google")

@google_router.get('/login')
async def login_via_google(request: Request):
    redirect_uri = request.url_for('authorize_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

async def get_google_user(request: Request):
    user = request.session.get('user')
    if user is None:
        return None
    return user

@google_router.get('/auth')
async def authorize_google(request: Request):
    if request.session.get('user') is None:
        try:
            token = await oauth.google.authorize_access_token(request)
        except Exception as e:
            return {'error': str(e)}
        user = token['userinfo']
        request.session['user'] = dict(user)
        return dict(user)
    else:
        return RedirectResponse(url='/')
