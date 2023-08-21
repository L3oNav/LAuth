from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime

class Model(DeclarativeBase):

    created_at = Column(DateTime, nullable=False, server_default='now()')
    updated_at = Column(DateTime, nullable=False, server_default='now()', onupdate='now()')
