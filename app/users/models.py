from app.settings.base_model import Model
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(50))
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True, default=None)
    accounts = relationship("Account", back_populates="user")



class Account(Model):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    issuer = Column(String(32), nullable=False)
    subject = Column(String(32), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="accounts")
