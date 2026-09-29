import uuid
from typing import Optional, List
from sqlalchemy import String, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from .base import Base, TimestampMixin, OptimisticMixin, TenantMixin

class Enterprise(Base, TimestampMixin, OptimisticMixin):
    __tablename__ = "enterprises"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="free")
    
    users: Mapped[List["User"]] = relationship(back_populates="enterprise")

class UserRole(str, Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    AGENT = "agent"

class User(Base, TimestampMixin, OptimisticMixin, TenantMixin):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.AGENT)
    
    enterprise: Mapped["Enterprise"] = relationship(back_populates="users")

class ChannelType(str, Enum):
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    EMAIL = "email"

class Channel(Base, TimestampMixin, TenantMixin):
    __tablename__ = "channels"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[ChannelType] = mapped_column(SQLEnum(ChannelType))
    name: Mapped[str] = mapped_column(String(100))
    credentials: Mapped[dict] = mapped_column(JSON)  # Encrypted in business logic layer
    is_active: Mapped[bool] = mapped_column(default=True)

class Contact(Base, TimestampMixin, TenantMixin):
    __tablename__ = "contacts"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    external_id: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    
    conversations: Mapped[List["Conversation"]] = relationship(back_populates="contact")

class ConversationStatus(str, Enum):
    OPEN = "open"
    PENDING = "pending"
    RESOLVED = "resolved"

class Conversation(Base, TimestampMixin, OptimisticMixin, TenantMixin):
    __tablename__ = "conversations"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    contact_id: Mapped[uuid.UUID] = mapped_column(uuid.UUID, ForeignKey("contacts.id"))
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(uuid.UUID, ForeignKey("users.id"))
    status: Mapped[ConversationStatus] = mapped_column(SQLEnum(ConversationStatus), default=ConversationStatus.OPEN)
    
    contact: Mapped["Contact"] = relationship(back_populates="conversations")

class Message(Base, TimestampMixin, TenantMixin):
    __tablename__ = "messages"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(uuid.UUID, ForeignKey("conversations.id"))
    sender_type: Mapped[str] = mapped_column(String(20)) # 'agent' or 'client'
    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(uuid.UUID) # Can be User.id if agent
    content: Mapped[str] = mapped_column(Text)
    external_id: Mapped[Optional[str]] = mapped_column(String(255))
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON)