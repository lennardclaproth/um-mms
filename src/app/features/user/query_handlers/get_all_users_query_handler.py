from datetime import datetime
from typing import List
import uuid
from app.app_context import AppContext
from app.context.user import User
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.repositories.user_repository import UserRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.cryptography.password_manager import PasswordManager
from common.dependency_injection.auto_wire import AutoWire
from common.mediator.cqrs import CommandHandler, QueryHandler
from common.mediator.sender import Sender


class GetAllUsersQueryHandler(QueryHandler[GetAllUsersQuery, List[User]], metaclass=AutoWire):

    def __init__(self, user_repository: UserRepositoryInterface, app_context: AppContext):
        super().__init__()
        self._user_repository = user_repository
        self._app_context = app_context

    def handle(self, query) -> List[User]:
        if (self._app_context.logged_in_user.role.decode() == '1'):
            return [self._user_repository.get_user_by_username(self._app_context.logged_in_user.username)]
        return self._user_repository.get_users()
