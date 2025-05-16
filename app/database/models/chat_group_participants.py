from advanced_alchemy.base import orm_registry
from sqlalchemy import Column, ForeignKey, Table

chat_group_participant_association = Table(
    "chat_group_participants",
    orm_registry.metadata,
    Column("user_id", ForeignKey("user_accounts.id", ondelete="CASCADE"), primary_key=True),
    Column("chat_group_id", ForeignKey("chat_groups.id", ondelete="CASCADE"), primary_key=True),
)
