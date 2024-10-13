
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
from app.features.user.commands.create_user_command import CreateUserCommand
from app.features.user.commands.delete_user_command import DeleteUserCommand
from app.features.user.commands.update_user_command import UpdateUserCommand
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.features.user.validators.user_password_validator import UserPasswordValidator
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.action import ActionInterface
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender
from common.validation.validator import ValidationError


class ResetUserPasswordAction(ActionInterface[User], metaclass=AutoWire):
    def __init__(self, sender: Sender, logger: LoggerInterface, app_context: AppContext):
        super().__init__()
        self._sender = sender
        self._logger = logger
        self._app_context = app_context

    def act(self, input: User, page: 'PageInterface') -> None:
        if (self._app_context.logged_in_user.role.decode() == '2'):
            if (input.role.decode() != '1'):
                self._logger.warning(f"A user tried to change the password of a user with more permissions {ROLE(2)}", action="Reset user password",
                                     username=self._app_context.logged_in_user.username.decode(), user_to_update=input.username.decode())
                raise ValueError(
                    "You are not allowed to update the password of an user with more permissions then you. Activity logged")

        validator = UserPasswordValidator()
        if validator.validate(input) == False:
            raise ValidationError(validator._errors)

        self._sender.send(UpdateUserCommand(input, attribute="password"))

        self._logger.info("Password succesfully updated", action="Reset user password",
                          actor=self._app_context.logged_in_user.username.decode(), deleted_user_username=input.username.decode())

        return page.options.get('1')
