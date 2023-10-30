from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache
import os
load_dotenv()

class Settings(BaseSettings):

    APP_NAME: str = "lnav-auth-service"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENVIROMENT: str = os.getenv("ENVIROMENT", "development")
    ACCESS_TOKEN_EXPIRATION_MINUTES: int = 1440
    OBJECT_STORAGE_ACCESS_KEY: str = os.getenv("OBJECT_STORAGE_ACCESS_KEY")
    OBJECT_STORAGE_SECRET_KEY: str = os.getenv("OBJECT_STORAGE_SECRET_KEY")
    OBJECT_STORAGE_ENDPOINT_PUBLIC: str = os.getenv("OBJECT_STORAGE_ENDPOINT_PUBLIC")
    OBJECT_STORAGE_ENDPOINT_PRIVATE: str = os.getenv("OBJECT_STORAGE_ENDPOINT_PRIVATE")
    OBJECT_STORAGE_REGION: str = os.getenv("OBJECT_STORAGE_REGION")
    GOOGLE_ID_CLIENT: str = os.getenv("GOOGLE_ID_CLIENT")
    GOOGLE_SECRET_CLIENT: str = os.getenv("GOOGLE_SECRET_CLIENT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

@lru_cache()
def get_settings():
    return Settings()
