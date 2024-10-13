from app.app import App
from app.context.unique_meal_db_context import UniqueMealDbContext
from common.dependency_injection.auto_wire import AutoWire
from common.dependency_injection.container import Container
from common.dependency_injection.lifetimes import Lifetime
from common.inter_act.engine import Engine
from common.mediator.sender import Sender
from common.smart_db.context import DbContext


class Builder:

    container = None
    app = None

    def __init__(self):
        pass

    def add_dependency_injection(self):
        self.container = Container()
        AutoWire.container = self.container

    def add_service(self, interface, implementation, lifetime: Lifetime):
        if (self.container == None):
            raise Exception(
                "You cannot register a service if the container has not been setup yet.")

        if (lifetime == Lifetime.SCOPED):
            self.container.register_as_scoped(interface, implementation)
            return

        if (lifetime == Lifetime.SINGLETON):
            self.container.register_as_singleton(interface, implementation)
            return

        if (lifetime == Lifetime.TRANSIENT):
            self.container.register_as_transient(interface, implementation)
            return

    def add_mediator(self):
        self.container.register_as_singleton(Sender, Sender)

    def add_logging(self):
        pass

    def add_secure_database_access(self):
        self.container.register_as_singleton(
            DbContext, UniqueMealDbContext)
        unique_meal_db_context: UniqueMealDbContext = self.container.resolve(
            DbContext)
        unique_meal_db_context.initialize_db()

    def build_app(self):
        self.app = App()

    def add_render_engine(self, stdscr, view_stack_size):
        self.container.register_as_singleton(Engine, Engine)
        engine: Engine = self.container.resolve(Engine)
        engine.initialize_engine(stdscr, view_stack_size)
