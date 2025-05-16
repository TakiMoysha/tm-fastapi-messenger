from logging import getLogger

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, SQLAlchemyAsyncQueryService
from fastapi import status

from app.database.models.chat import ChatModel
from app.exceptions import PermissionDeniedException, WorkInProgressException

EXC_ = ""

logger = getLogger(__name__)

__all__ = ("ChatService",)


class ChatService(SQLAlchemyAsyncQueryService[ChatModel]):
    repository_type = ChatRepository
    match_fields = ["id", "slug"]
