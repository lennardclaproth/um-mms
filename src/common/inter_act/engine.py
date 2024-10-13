import curses
import app
from app.app_context import AppContext
from app.context.user import User
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.registry import Registry
from common.inter_act.view_stack import ViewStack
from common.logging.logger import LoggerInterface


class Engine(metaclass=AutoWire):

    def __init__(self, app_context: AppContext, logger: LoggerInterface):
        self._app_context = app_context
        self._logger = logger

    def initialize_engine(self, stdscr, view_stack_size):
        self.registry = Registry()
        self.view_stack: ViewStack = ViewStack(view_stack_size)
        self.registry.scan_and_register(app)
        self.screen = stdscr
        self.__initialize_curses()
        self.size = self.screen.getmaxyx()

    def __prepare_screen(self):
        self.screen.clear()
        self.screen.border(0)
        self.screen.refresh()

    def __initialize_curses(self):
        curses.curs_set(0)
        self.screen.border(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def get_menu(self):
        from app.features.user.pages.user_menu import UserMenu
        from app.view.main_menu import MainMenu
        logged_in_user: User | None = self._app_context.logged_in_user
        if logged_in_user is not None:
            return self.registry.get_page(UserMenu)
        return self.registry.get_page(MainMenu)

    def render(self, view: 'PageInterface'):
        from app.view.main_menu import MainMenu
        from app.features.user.pages.user_menu import UserMenu
        if view is 'q':
            return view
        if view == MainMenu:
            logged_in_user: User | None = self._app_context.logged_in_user
            if logged_in_user is not None:
                view = self.registry.get_page(UserMenu)
            else:
                view = self.registry.get_page(MainMenu)
        else:
            view = self.registry.get_page(view)
        self.__prepare_screen()
        self.view_stack.add_value(view)
        view.render(self.size)
        return view.perform_action()
