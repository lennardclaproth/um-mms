
from app.app_context import AppContext
from app.context.member import Member
from app.context.user import User
from app.features.member.commands.delete_member_command import DeleteMemberCommand
from app.features.user.commands.create_user_command import CreateUserCommand
from app.features.user.commands.delete_user_command import DeleteUserCommand
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.features.user.validators.user_validator import UserValidator
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.action import ActionInterface
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender


class DeleteMemberAction(ActionInterface[Member], metaclass=AutoWire):
    def __init__(self, sender: Sender, logger: LoggerInterface, app_context: AppContext):
        super().__init__()
        self._sender = sender
        self._logger = logger
        self._app_context = app_context

    def act(self, input: Member, page: 'PageInterface') -> None:
        self._sender.send(DeleteMemberCommand(input))

        self._logger.info("Member successfully deleted", action="Deleted member action",
                          actor=self._app_context.logged_in_user.username.decode(), deleted_member_membership_id=input.membership_id.decode())

        return page.options.get('1')
