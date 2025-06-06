from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from advanced_alchemy.types import FileObject, StoredObject
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import get_config

if TYPE_CHECKING:
    from .user import UserModel
    from .chat import ChatModel
    from .chat_group import ChatGroupModel


config = get_config()


# (id, chat_id, sender_id, text, timestamp, is_read)
class ChatMessageModel(UUIDv7AuditBase):
    """
    Attributes:
        id:

        chat_id:
        sender_id:
        text:
        timestamp:
        is_read:

        attachment:

        chat:
        sender:

        created_at:
        updated_at:
    """

    __tablename__ = "chat_messages"
    __table_args__ = {"comment": "users messages in chats"}
    __pii_columns__ = {}

    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("user_accounts.id", ondelete="CASCADE"), nullable=True)
    text: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(UTC))
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)

    attachment: Mapped[FileObject | None] = mapped_column(
        StoredObject(backend=config.storage.get_default_storage(), multiple=True),
        nullable=True,
        default=None,
    )

    # ============================== Relationships

    chat: Mapped["ChatModel"] = relationship(back_populates="messages", lazy="selectin", uselist=False)
    sender: Mapped["UserModel"] = relationship(back_populates="sent_messages", lazy="selectin", uselist=False)
