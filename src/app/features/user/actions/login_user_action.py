
from app.app_context import AppContext
from app.context.user import User
from app.features.user.commands.create_user_command import CreateUserCommand
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.features.user.queries.login_user_query import LoginUserQuery
from app.features.user.validators.user_validator import UserValidator
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.action import ActionInterface
from common.inter_act.page import PageInterface
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender


class LoginUserAction(ActionInterface[User], metaclass=AutoWire):
    def __init__(self, sender: Sender, app_context: AppContext, logger: LoggerInterface):
        super().__init__()
        self._sender = sender
        self._app_context = app_context
        self._logger = logger

    def act(self, input: User, page: PageInterface):
        if (self._app_context.failed_login_attempts >= 3):
            self._logger.warning(
                "Too many login attempts", activity="User log in", attempted_username=input.username.decode())
            self._app_context.should_log = False
            raise ValueError("Too many login attempts. Activity logged.")
        user = self._sender.send(LoginUserQuery(
            input.username, input.password))
        if user is not None:
            self._app_context.logged_in_user = user
            self._logger.info("User succesfully logged in.", activity="User log in",
                              suspicious="No", username=self._app_context.logged_in_user.username.decode())
            self._app_context.should_log = False
            return page.options.get('1')
        self._app_context.failed_login_attempts += 1
        self._app_context.should_log = False
        raise ValueError("Wrong username or password")
