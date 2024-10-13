from typing import List
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
from app.features.logging.pages.logging_view_log_page import LoggingViewLogPage
from app.features.logging.queries.get_all_logs_query import GetAllLogsQuery
from app.features.member.actions.create_member_action import CreateMemberAction
from app.context.member import Member
from app.features.user.actions.create_user_action import CreateUserAction
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.view.error_page import ErrorPage
from app.view.main_menu import MainMenu
from app.view.success_page import SuccessPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.input import Input
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page
from common.logging.log import Log
from common.mediator.sender import Sender


class LoggingViewPage(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine, app_context: AppContext, sender: Sender):
        self._action = engine.registry.get_action(CreateUserAction)
        self.user = User
        self._app_context = app_context
        self._sender = sender
        super().__init__(engine=engine)
        self.options.update({
            '1': LoggingViewLogPage,
            'm': MainMenu
        })

    def render_header(self, size):
        return TextBox.get_component(size, 2, f'Viewing all users').refresh()

    def render_body(self, size):
        logs: List[Log] = self._sender.send(GetAllLogsQuery())

        view_items = ['No logs yet']
        if logs is not None and len(logs) > 0:
            view_items = []
            for i in range(len(logs)):
                view_items.append(
                    f"{logs[i].str_repr}")
        screen = Screen(view_items, size, 3, width=100, should_truncate=True)
        selected_log = screen.run()
        try:
            if selected_log == 'm' or selected_log == 'q':
                self.selected_option = selected_log
            else:
                index = int(selected_log) - 1
                self._app_context.selected_log = logs[index]
                self.selected_option = '1'
        except Exception as e:
            raise ValueError(
                f'Error occured while trying to parse the index of the selected transaction\nNested exception is: {e}')

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            a = False
        return self.options.get(self.selected_option)

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit UM-MMS 🛑'
        TextBox.get_component(size, 10, text, size[0]-3).refresh()

    def render(self, size):
        self.render_header(size)
        self.render_footer(size)
        self.render_body(size)
