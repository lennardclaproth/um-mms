from datetime import datetime
import uuid
from app.app_context import AppContext
from app.constants import ROLE
from app.features.member.commands.delete_member_command import DeleteMemberCommand
from app.features.user.commands.delete_user_command import DeleteUserCommand
from app.repositories.member_repository import MemberRepositoryInterface
from app.repositories.user_repository import UserRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.cryptography.password_manager import PasswordManager
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.mediator.cqrs import CommandHandler
from app.features.user.commands.create_user_command import CreateUserCommand
from common.mediator.sender import Sender


class DeleteMemberCommandHandler(CommandHandler[DeleteMemberCommand], metaclass=AutoWire):

    def __init__(self, sender: Sender, member_repository: MemberRepositoryInterface, encoder: Encoder, app_context: AppContext, logger: LoggerInterface):
        super().__init__()
        self._encoder = encoder
        self._app_context = app_context
        self._sender = sender
        self._member_repository = member_repository
        self._logger = logger

    def handle(self, command):
            
        self._member_repository.delete_member(command.member)
