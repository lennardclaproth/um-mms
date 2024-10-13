from datetime import datetime
import uuid
from app.constants import ROLE
from app.repositories.user_repository import UserRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.cryptography.password_manager import PasswordManager
from common.dependency_injection.auto_wire import AutoWire
from common.mediator.cqrs import CommandHandler
from app.features.user.commands.update_user_command import UpdateUserCommand
from common.mediator.sender import Sender


class UpdateUserCommand(CommandHandler[UpdateUserCommand], metaclass=AutoWire):

    def __init__(self, user_repository: UserRepositoryInterface, encoder: Encoder, password_manager: PasswordManager):
        super().__init__()
        self._encoder = encoder
        self._user_repository = user_repository
        self._password_manager = password_manager

    def handle(self, command):
        if command.attribute == "password":
            command.user.password = self._password_manager.hash_password(
            command.user.password).encode('utf-8')

        self._user_repository.update_user(command.user, command.attribute)
