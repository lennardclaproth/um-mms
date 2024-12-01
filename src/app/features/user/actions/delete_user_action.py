
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
from app.features.user.commands.create_user_command import CreateUserCommand
from app.features.user.commands.delete_user_command import DeleteUserCommand
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.features.user.validators.user_validator import UserValidator
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.action import ActionInterface
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender


class DeleteUserAction(ActionInterface[User], metaclass=AutoWire):
    def __init__(self, sender: Sender, logger: LoggerInterface, app_context: AppContext):
        super().__init__()
        self._sender = sender
        self._logger = logger
        self._app_context = app_context

    def act(self, input: User, page: 'PageInterface') -> None:
        if (self._app_context.logged_in_user.role.decode() == '2'):
            if (input.role.decode() != '1'):
                self._logger.warning(f"A user tried to remove a user with more permissions, expected role {ROLE(b'2')}", action="Delete user action",
                                     username=self._app_context.logged_in_user.username.decode(), user_role=ROLE(self._app_context.logged_in_user.role), user_to_delete=input.username.decode())
                self._app_context.should_log = False
                raise ValueError(
                    "You are not allowed to delete an user with more permissions then you. Activity logged.")

        self._sender.send(DeleteUserCommand(input))

        self._logger.info("User successfully deleted", action="Deleted user action",
                          actor=self._app_context.logged_in_user.username.decode(), deleted_user_username=input.username.decode())

        return page.options.get('1')
