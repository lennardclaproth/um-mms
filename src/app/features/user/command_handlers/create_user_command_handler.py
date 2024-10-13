from datetime import datetime
import uuid
from app.constants import ROLE
from app.repositories.user_repository import UserRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.cryptography.password_manager import PasswordManager
from common.dependency_injection.auto_wire import AutoWire
from common.mediator.cqrs import CommandHandler
from app.features.user.commands.create_user_command import CreateUserCommand
from common.mediator.sender import Sender


class CreateUserCommand(CommandHandler[CreateUserCommand], metaclass=AutoWire):

    def __init__(self, sender: Sender, user_repository: UserRepositoryInterface, encoder: Encoder, password_manager: PasswordManager):
        super().__init__()
        self._encoder = encoder
        self._password_manager = password_manager
        self._sender = sender
        self._user_repository = user_repository

    def handle(self, command):
        command.user.id = str(uuid.uuid4()).encode('utf-8')
        command.user.registration_date = datetime.now().isoformat().encode('utf-8')

        if command.user.username == b'super_admin' and ROLE(command.user.role) == b'super_admin':
            if len(self._user_repository.get_users_by_username(command.user.username)) > 0:
                return
            command.user.first_name = "Super".encode('utf-8')
            command.user.last_name = "Admin".encode('utf-8')

        command.user.password = self._password_manager.hash_password(
            command.user.password).encode('utf-8')

        self._user_repository.create_user(command.user)
