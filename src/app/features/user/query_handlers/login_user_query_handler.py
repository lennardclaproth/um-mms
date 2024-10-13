from app.context.user import User
from app.features.user.queries.login_user_query import LoginUserQuery
from app.repositories.user_repository import UserRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.cryptography.password_manager import PasswordManager
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.mediator.cqrs import QueryHandler


class LoginUserQueryHandler(QueryHandler[LoginUserQuery, User], metaclass=AutoWire):

    def __init__(self, user_repository: UserRepositoryInterface, password_manager: PasswordManager, encoder: Encoder, logger: LoggerInterface):
        super().__init__()
        self._user_repository = user_repository
        self._password_manager = password_manager
        self._encoder = encoder
        self._logger = logger

    def handle(self, query):
        user = self._user_repository.get_user_by_username(
            query.username)
        if user is None:
            self._logger.info("Failed log in attempt, user does not exist.",
                              activity="User log in", suspicious="No", username=query.username.decode())
            return user
        if self._password_manager.verify_password(user.password, query.password):
            return user
        else:
            self._logger.info("Failed log in attempt, password is incorrect.",
                              activity="User log in", suspicious="No", username=query.username.decode())
