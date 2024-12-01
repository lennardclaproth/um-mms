from app.app_context import AppContext
from app.context.user import User
from app.features.user.commands.create_user_command import CreateUserCommand
from app.view.error_page import ErrorPage
from app.view.main_menu import MainMenu
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.engine import Engine
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender
from common.smart_db.context import DbContext
from common.validation.validator import ValidationError


class App(metaclass=AutoWire):

    def __init__(self, engine: Engine, app_context: AppContext, sender: Sender, db_context: DbContext, logger: LoggerInterface):
        self._engine = engine
        self._app_context = app_context
        self._sender = sender
        self._db_context = db_context
        self._logger = logger

    def start(self):
        self._logger.info("Starting application")
        super_admin = User
        super_admin.username = "super_admin".encode('utf-8')
        super_admin.password = "Admin_123?".encode('utf-8')
        super_admin.role = '3'.encode('utf-8')

        self._sender.send(CreateUserCommand(super_admin))

        next = self._engine.render(MainMenu)

        self._logger.info("Application successfully started")

        while next != 'q':
            AutoWire.container.clear_scope()
            try:
                next = self._engine.render(next)
            except Exception as e:
                if not isinstance(e, ValidationError):
                    if self._app_context.logged_in_user == None and self._app_context.should_log:
                        self._logger.error("An error occurred.", error=str(e))
                    elif self._app_context.should_log:
                        self._logger.error("An error occurred.", error=str(e),
                                           logged_in_user=self._app_context.logged_in_user.username)
                self._app_context.should_log == True
                self._app_context.error = e
                self._app_context.state = "Error"
                self._db_context.close_db()
                next = self._engine.render(ErrorPage)
                # State.instance(Error).set_value(e)
                # next_action = render_engine.load(ErrorPage)
