
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
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


class UpdateUserAction(ActionInterface[User], metaclass=AutoWire):
    def __init__(self, sender: Sender, logger: LoggerInterface, app_context: AppContext):
        super().__init__()
        self._sender = sender
        self.logger = logger
        self._app_context = app_context

    def act(self, input: User, page: 'PageInterface', **kwargs) -> None:
        if (self._app_context.logged_in_user.role.decode() == '2' and self._app_context.logged_in_user.username.decode() != input.username.decode()):
            if (input.role.decode() != '1'):
                self.logger.warning(f"A user tried to change data of a user with more permissions, should expect role {ROLE(b'2')}", action="Update user action",
                                    username=self._app_context.logged_in_user.username.decode(), user_to_update=input.username.decode(), role=ROLE(self._app_context.logged_in_user.role),)
                raise ValueError(
                    "You cannot edit an user with the same or more permissions as you. Activity has been logged.")

        if (self._app_context.logged_in_user.role.decode() == '3' and self._app_context.logged_in_user.username.decode() != input.username.decode()):
            if (input.role.decode() == '3'):
                self.logger.warning(f"A user tried to change data of a user with more permissions, should expect role {ROLE(b'3')}", action="Update user action",
                                    username=self._app_context.logged_in_user.username.decode(), role=ROLE(self._app_context.logged_in_user.role), user_to_update=input.username.decode())
                raise ValueError(
                    "You cannot edit an user with the same permissions as you. Activity has been logged.")

        validator = UpdateUserValidator()

        if validator.validate(input) == False:
            raise ValidationError(validator._errors)

        self._sender.send(UpdateUserCommand(
            input, attribute=kwargs.get('attribute')))

        self.logger.info(f"User successfully updated, updated {kwargs.get('attribute')}", action="Update user action",
                         actor=self._app_context.logged_in_user.username.decode(), updated_user_username=input.username.decode())

        return page.options.get('1')
