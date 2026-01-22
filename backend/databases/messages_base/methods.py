from pymongo.collection import Collection
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import MessagesResponse, SendMessagesRequestModel
from backend.errors import InvalidMessagesError, NoReadPermissionError, NoWritePermissionError
from backend.databases.data_base.data_methods import get_user_chats
from pydantic import ValidationError

async def add_messages(
    user_id: int,
    messages: SendMessagesRequestModel,
    session: AsyncSession,
    collection: Collection
) -> None:
    avarible_chats = await get_user_chats(user_id, session)
    for message in messages.messages:
        if message.chat_id not in avarible_chats:
            raise NoWritePermissionError(message)
    
    try:
        await collection.insert_many(messages.model_dump()["messages"])
    except TypeError:
        raise InvalidMessagesError()
    except ValidationError as e:
        raise InvalidMessagesError(e.errors())
    
async def get_messages_by_chat(
        user_id: int,
        chat_id: str,
        collection: Collection,
        session: AsyncSession,
        limit: int = 50,
        offset: int = 0
) -> MessagesResponse:
    avarible_chats = await get_user_chats(user_id, session)
    if chat_id in avarible_chats:
        messages = await collection.find(
            {"chat_id": chat_id},
            {"_id": 0}
        ).skip(offset).limit(limit).to_list(length=limit)
        return MessagesResponse.model_validate({"messages": messages})
    
    raise NoReadPermissionError()
