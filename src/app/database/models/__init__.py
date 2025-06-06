from .user import UserModel
from .chat import ChatModel
from .chat_group import ChatGroupModel
from .chat_message import ChatMessageModel
from .chat_group_participants import chat_group_participant_association


def get_models():
    return [
        UserModel,
        ChatModel,
        ChatGroupModel,
        ChatMessageModel,
        chat_group_participant_association,
    ]


__all__ = (
    "UserModel",
    "ChatModel",
    "ChatGroupModel",
    "ChatMessageModel",
    "chat_group_participant_association",
)
