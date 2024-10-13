from datetime import datetime
import random
import uuid
from app.repositories.member_repository import MemberRepositoryInterface
from app.features.member.commands.create_member_command import CreateMemberCommand
from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from common.mediator.cqrs import CommandHandler
from common.mediator.sender import Sender


class CreateMemberCommandHandler(CommandHandler[CreateMemberCommand], metaclass=AutoWire):

    def __init__(self, sender: Sender, member_repository: MemberRepositoryInterface, encoder: Encoder):
        super().__init__()
        self._sender = sender
        self._member_repository = member_repository
        self._encoder = encoder

    def handle(self, command):
        command.member.id = str(uuid.uuid4()).encode('utf-8')
        command.member.membership_id = str(
            self.create_membership_id()).encode('utf-8')
        command.member.registration_date = datetime.now().isoformat().encode('utf-8')
        command.member.phonenumber = b"+31-6-" + command.member.phonenumber

        self._member_repository.create_member(command.member)

    def create_membership_id(self) -> str:
        current_year = datetime.now().year % 100
        year_str = f"{current_year:02}"
        middle_digits = ''.join(random.choices('0123456789', k=7))
        first_nine = year_str + middle_digits
        checksum = sum(int(digit) for digit in first_nine) % 10
        final_string = first_nine + str(checksum)
        return final_string
