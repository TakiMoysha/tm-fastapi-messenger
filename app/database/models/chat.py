from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .chat_group import ChatGroupModel
    from .chat_message import ChatMessageModel
    from .user import UserModel


class ChatGroupKind(Enum):
    PRIVATE = "private"
    GROUP = "group"


# (id, title, type: private/group)
class ChatModel(BigIntAuditBase):
    """
    Attributes:
        id:

        title:
        kind:
        creator_id:

        created_at:
        updated_at:
    """

    __tablename__ = "chats"
    __table_args__ = {"comment": "chats for users"}
    __pii_columns__ = {}

    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    # slug: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    kind: Mapped[ChatGroupKind] = mapped_column(default=ChatGroupKind.PRIVATE, nullable=False)
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("user_accounts.id", ondelete="CASCADE"), nullable=False)

    # ============================== Relationships

    creator: Mapped["UserModel"] = relationship(
        back_populates="chats",
        cascade="all, delete",
    )
    messages: Mapped[list["ChatMessageModel"]] = relationship(
        back_populates="chat",
        cascade="all, delete",
    )
    group: Mapped["ChatGroupModel"] = relationship(
        back_populates="chat",
        cascade="all, delete",
    )
