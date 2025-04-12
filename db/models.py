from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    gmail_id = Column(String, unique=True, index=True, nullable=False)
    sender = Column(String)
    recipient = Column(String)
    subject = Column(String)
    message_snippet = Column(String)
    received_at = Column(DateTime)
    labels = Column(JSON)
    is_read = Column(Boolean, default=False)