from app.app_context import AppContext
from app.context.user import User
from app.features.member.actions.create_member_action import CreateMemberAction
from app.context.member import Member
from app.features.member.actions.delete_member_action import DeleteMemberAction
from app.features.user.actions.create_user_action import CreateUserAction
from app.features.user.actions.delete_user_action import DeleteUserAction
from app.view.error_page import ErrorPage
from app.view.main_menu import MainMenu
from app.view.success_page import SuccessPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.input import Input
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page
from common.inter_act.components.text import Text


class MemberDeletePage(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine, app_context: AppContext):
        self._action = engine.registry.get_action(DeleteMemberAction)
        self.member = app_context.selected_member
        self._engine = engine
        super().__init__(engine=self._engine)
        self.options.update({
            '1': SuccessPage,
            '2': ErrorPage,
            'm': MainMenu
        })

    def render_header(self, size):
        text = 'Delete member'
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        text = 'Are you sure you want to delete the member? Press M to go back to the menu. Press any other button to delete the member.'
        Text.get_component(text, size).refresh()
        
    def perform_action(self):
        option = self._engine.screen.getch()
        if option == 'm':
            return option
        return self._action.act(input=self.member, page=self)

    def render_footer(self, size):
        return super().render_footer(size)

    def render(self, size):
        self.render_body(size)
        self.render_header(size)
