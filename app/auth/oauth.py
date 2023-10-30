from app.settings import get_settings
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth.register(
    name="google",
    client_id=get_settings().GOOGLE_ID_CLIENT,
    client_secret=get_settings().GOOGLE_SECRET_CLIENT,
    #access_token_url="https://accounts.google.com/o/oauth2/token",
    #access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={"scope": "openid profile email"},
)
