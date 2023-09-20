from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.settings import get_settings
from functools import lru_cache

user = get_settings().POSTGRES_USER
password = get_settings().POSTGRES_PASSWORD
hostname = get_settings().POSTGRES_HOST
db_name = get_settings().POSTGRES_DB

#engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{hostname}/{db_name}", pool_pre_ping=True)

@lru_cache
def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return Session

def get_session() -> Generator[scoped_session, None, None]:
    Session = create_session()
    try:
        yield Session
    finally:
        Session.remove()
