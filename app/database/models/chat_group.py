from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import UserModel
    from .chat import ChatModel


# (id, title, creator_id, participants)
class ChatGroupModel(BigIntAuditBase):
    """
    Attributes:
        id:

        created_at:
        updated_at:
    """

    __tablename__ = "chat_groups"
    __table_args__ = {"comment": "group of participants in chat"}
    __pii_columns__ = {"email"}

    title: Mapped[str] = mapped_column(String(length=255), nullable=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)

    # ============================== Relationships

    chat: Mapped["ChatModel"] = relationship(
        back_populates="groups",
        lazy="selectin",
        uselist=False,
        cascade="all, delete",
    )
    # participants: Mapped[list["UserModel"]] = relationship(
    #     back_populates="chat_groups",
    #     lazy="selectin",
    #     uselist=True,
    #     cascade="all, delete",
    # )
