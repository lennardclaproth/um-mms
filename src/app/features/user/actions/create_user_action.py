
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
from app.features.user.commands.create_user_command import CreateUserCommand
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.features.user.validators.user_validator import UserValidator
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.action import ActionInterface
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender
from common.validation.validator import ValidationError


class CreateUserAction(ActionInterface[User], metaclass=AutoWire):
    def __init__(self, sender: Sender, logger: LoggerInterface, app_context: AppContext):
        super().__init__()
        self._sender = sender
        self._logger = logger
        self._app_context = app_context

    def act(self, input: User, page: 'PageInterface') -> None:
        validator = UserValidator()

        if validator.validate(input) == False:
            raise ValidationError(validator._errors)

        if (self._app_context.logged_in_user.role.decode() == '2'):
            if (input.role.decode() != '1'):
                self._logger.warning(f"A user tried to create a user with more permissions, expected role {ROLE(b'2')}", action="Delete user action",
                                     username=self._app_context.logged_in_user.username.decode(), user_role=ROLE(self._app_context.logged_in_user.role), user_to_delete=input.username.decode())
                self._app_context.should_log = False
                raise ValueError(
                    "You are not allowed to create an user with more permissions then you.")

        if (self._app_context.logged_in_user.role.decode() == '3'):
            if (input.role.decode() == '3'):
                self._logger.warning(f"A user tried to create a super_admin", action="Delete user action",
                                     username=self._app_context.logged_in_user.username.decode(), user_role=ROLE(self._app_context.logged_in_user.role), user_to_delete=input.username.decode())
                self._app_context.should_log = False
                raise ValueError("You cannot create another super admin.")

        self._sender.send(CreateUserCommand(input))

        self._logger.info("User successfully created", action="Create user action",
                          actor=self._app_context.logged_in_user.username.decode(), created_user_username=input.username.decode())

        return page.options.get('1')
