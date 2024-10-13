from app.repositories.member_repository import MemberRepositoryInterface
from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.mediator.cqrs import CommandHandler
from app.features.member.commands.update_member_command import UpdateMemberCommand


class UpdateMemberCommand(CommandHandler[UpdateMemberCommand], metaclass=AutoWire):

    def __init__(self, member_repository: MemberRepositoryInterface, encoder: Encoder):
        super().__init__()
        self._encoder = encoder
        self._member_repository = member_repository

    def handle(self, command):
        self._member_repository.update_member(command.member, command.attribute)
