from app.settings.base_model import Model
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Model):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True, default=None)
