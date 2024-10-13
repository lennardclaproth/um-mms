from datetime import datetime
import uuid
from app.app_context import AppContext
from app.constants import ROLE
from app.features.user.commands.delete_user_command import DeleteUserCommand
from app.repositories.user_repository import UserRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.cryptography.password_manager import PasswordManager
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.mediator.cqrs import CommandHandler
from app.features.user.commands.create_user_command import CreateUserCommand
from common.mediator.sender import Sender


class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand], metaclass=AutoWire):

    def __init__(self, sender: Sender, user_repository: UserRepositoryInterface, encoder: Encoder, app_context: AppContext, logger: LoggerInterface):
        super().__init__()
        self._encoder = encoder
        self._app_context = app_context
        self._sender = sender
        self._user_repository = user_repository
        self._logger = logger

    def handle(self, command):
        if command.user.id == self._app_context.logged_in_user.id:
            self._logger.warning("A user tried to remove themselves", action="Delete user action",
                                    username=self._app_context.logged_in_user.username.decode())
            raise ValueError("You cannot delete yourself. Activity logged.")
        self._user_repository.delete_user(command.user)
