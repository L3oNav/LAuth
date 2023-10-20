from app.settings.base_model import Model
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Users(Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True, default=None)
    accounts = relationship(back_populates="users") 

class Accounts(Model):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    issuer = Column(String(32), nullable=False)
    subject = Column(String(32), nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship(back_populates="accounts")
