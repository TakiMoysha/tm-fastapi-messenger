from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .chat import ChatModel
from .chat_group import ChatGroupModel
from .chat_message import ChatMessageModel


def _groups():
    from .chat_group_participants import chat_group_participant_association

    return chat_group_participant_association


# (id, name, email, password)
class UserModel(UUIDAuditBase):
    """
    Attributes:
        id:

        email:
        hashed_password:
        is_superuser:

        created_at:
        updated_at:
    """

    __tablename__ = "user_accounts"
    __table_args__ = {"comment": "user accounts for application access"}
    __pii_columns__ = {"email"}

    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(length=255), nullable=True, default=None) # deferred=True
    # hashed_password: Mapped[str | None] = mapped_column(PasswordHash(backen=PwdlibHasher(hasher=PwdlibArgon2Hasher())))
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

    # ============================== Relationships

    chats: Mapped[list["ChatModel"]] = relationship(
        back_populates="creator",
        # lazy="joined",
        # innerjoin=True,
    )
    sent_messages: Mapped[list["ChatMessageModel"]] = relationship(
        back_populates="sender",
    )
    groups: Mapped[list["ChatGroupModel"]] = relationship(
        secondary=lambda: _groups(),
        back_populates="participants",
    )

    @hybrid_property
    def has_password(self) -> bool:
        return self.hashed_password is not None
