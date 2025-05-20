from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import UserModel
    from .chat import ChatModel


def _participants():
    from .chat_group_participants import chat_group_participant_association

    return chat_group_participant_association


# (id, title, creator_id, participants)
class ChatGroupModel(BigIntAuditBase):
    """
    Attributes:
        id:

        title:
        chat_id:

        created_at:
        updated_at:
    """

    __tablename__ = "chat_groups"
    __table_args__ = {"comment": "group of participants in chat"}
    __pii_columns__ = {"email"}

    title: Mapped[str] = mapped_column(String(length=255), nullable=True)
    # slug: Mapped[str]
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)

    # ============================== Relationships

    chat: Mapped["ChatModel"] = relationship(
        back_populates="group",
        lazy="selectin",
        uselist=False,
        cascade="all, delete",
    )
    participants: Mapped[list["UserModel"]] = relationship(
        secondary=lambda: _participants(),
        back_populates="groups",
    )
