from logging import getLogger

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.database.models.chat import ChatModel

EXC_ = ""

logger = getLogger(__name__)

__all__ = ("ChatService",)


class ChatService(SQLAlchemyAsyncRepositoryService[ChatModel]):
    class ChatRepository(SQLAlchemyAsyncRepository[ChatModel]):
        model_type = ChatModel

    repository_type = ChatRepository
    match_fields = ["id"]
