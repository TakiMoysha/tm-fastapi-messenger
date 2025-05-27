from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import UserModel
    from .chat import ChatModel
    from .chat_group import ChatGroupModel
    from .chat_message import ChatMessageModel


def _groups():
    from .chat_group_participants import chat_group_participant_association

    return chat_group_participant_association


class RefreshToken(UUIDAuditBase):
    """
    Attributes:
        user_id: UUID
        refresh_token: str
        expires_in: int
        fingerprint: str | None
    """

    __tablename__ = "user_refresh_tokens"
    __table_args__ = {"comment": "user refresh tokens"}
    __pii_columns__ = {}

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_accounts.id", ondelete="CASCADE"), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(length=255), nullable=False)
    expires_in: Mapped[int] = mapped_column(nullable=False)
    fingerprint: Mapped[str | None] = mapped_column(String(length=255), nullable=True, default=None)

    # ============================== Relationships

    user: Mapped["UserModel"] = relationship(back_populates="refresh_tokens")
