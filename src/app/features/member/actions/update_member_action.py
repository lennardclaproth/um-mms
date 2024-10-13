
from logging import Logger
from app.app_context import AppContext
from app.context.member import Member
from app.context.user import User
from app.features.member.commands.update_member_command import UpdateMemberCommand
from app.features.member.validators.member_validator import MemberValidator
from app.features.member.validators.update_member_validator import UpdateMemberValidator
from app.features.user.commands.create_user_command import CreateUserCommand
from app.features.user.commands.update_user_command import UpdateUserCommand
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.features.user.validators.update_user_validator import UpdateUserValidator
from app.features.user.validators.user_validator import UserValidator
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.action import ActionInterface
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender
from common.validation.validator import ValidationError


class UpdateMemberAction(ActionInterface[Member], metaclass=AutoWire):
    def __init__(self, sender: Sender, logger: LoggerInterface, app_context: AppContext):
        super().__init__()
        self._sender = sender
        self._app_context = app_context
        self._logger = logger

    def act(self, input: Member, page: 'PageInterface', **kwargs) -> None:
        validator = UpdateMemberValidator()

        if validator.validate(input) == False:
            raise ValidationError(validator._errors)

        self._sender.send(UpdateMemberCommand(
            input, attribute=kwargs.get('attribute')))

        self._logger.info(f"Member successfully updated, updated {kwargs.get('attribute')}", action="Update member action",
                          actor=self._app_context.logged_in_user.username.decode(), updated_membership_id=input.membership_id.decode())

        return page.options.get('1')
