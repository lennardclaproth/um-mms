from app.app_context import AppContext
from app.context.user import User
from app.features.member.actions.create_member_action import CreateMemberAction
from app.context.member import Member
from app.features.member.actions.update_member_action import UpdateMemberAction
from app.features.user.actions.create_user_action import CreateUserAction
from app.features.user.actions.update_user_action import UpdateUserAction
from app.view.error_page import ErrorPage
from app.view.success_page import SuccessPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.input import Input
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class MemberUpdateStreetPage(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine, app_context: AppContext):
        self._action = engine.registry.get_action(UpdateMemberAction)
        self._app_context = app_context
        super().__init__(engine=engine)
        self.options.update({
            '1': SuccessPage,
            '2': ErrorPage
        })

    def render_header(self, size):
        text = 'Processing request please wait... 🔨'
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        self._app_context.selected_member.street = Input.get_component("Please enter the street name", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})

    def perform_action(self):
        return self._action.act(input=self._app_context.selected_member, page=self, attribute='street')

    def render_footer(self, size):
        return super().render_footer(size)

    def render(self, size):
        self.render_body(size)
        self.render_header(size)
