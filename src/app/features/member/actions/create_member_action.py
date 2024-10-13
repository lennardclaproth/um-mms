from app.constants import CITIES, GENDERS
from app.context.member import Member
from app.features.member.commands.create_member_command import CreateMemberCommand
from app.features.member.validators.member_validator import MemberValidator
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.action import ActionInterface
from common.inter_act.page import PageInterface
from common.mediator.sender import Sender
from common.validation.validator import ValidationError


class CreateMemberAction(ActionInterface[Member], metaclass=AutoWire):

    def __init__(self, sender: Sender):
        self._sender = sender
        self._cities = CITIES
        self._genders = GENDERS
        super().__init__()

    def act(self, input: Member, page: PageInterface):
        validator = MemberValidator()

        if validator.validate(input) == False:
            raise ValidationError(validator._errors)
            
        self._sender.send(CreateMemberCommand(input))

        return page.options.get('1')
