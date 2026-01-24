from fastapi import Depends
from typing import Annotated

from backend.utils import services
from backend.dependencies import annotations

from backend.repositories.data_methods import ChatRepository, DataRepository
from backend.repositories.auth_methods import AuthRepository
from backend.repositories.chat_methods import MessagesRepository

# TODO добавить фабрики для репозиториев

def get_auth_service(
    session: annotations.Database
) -> services.AuthService:
    auth_repo = AuthRepository(session)
    return services.AuthService(auth_repo)

def get_data_service(
    session: annotations.Database,
    collection: annotations.MessageBase
) -> services.DataService:
    data_repo = DataRepository(session)
    chats_repo = ChatRepository(session)
    mess_repo = MessagesRepository(collection, session)
    return services.DataService(data_repo, chats_repo, mess_repo)

AuthServiceDep = Annotated[services.AuthService, Depends(get_auth_service)]
DataServiceDep = Annotated[services.DataService, Depends(get_data_service)]