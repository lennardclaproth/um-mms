from app.context.user import User
from app.features.user.actions.login_user_action import LoginUserAction
from app.view.error_page import ErrorPage
from app.view.success_page import SuccessPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.input import Input
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class UserLoginPage(Page, metaclass=AutoWire):
    def __init__(self, engine: Engine):
        super().__init__(engine=engine)
        self.options.update({
            '1': SuccessPage,
            '2': ErrorPage
        })
        self.user = User
        self._engine = engine
        self._action = engine.registry.get_action(LoginUserAction)

    def render_header(self, size):
        extra_padding = 3
        text = 'Logging in please wait... 🔨'
        return TextBox.get_component(size, extra_padding, text)

    def render_body(self, size):
        self.user.username = Input.get_component(
            "Enter your username", {'height': 5, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.user.password = Input.get_component(
            "Enter your password", {'height': 5, 'width': 100, 'y': 6, 'x': 1, 'input_y': 1})

    def render_footer(self, size):
        super().render_footer(size)

    def perform_action(self):
        return self._action.act(input=self.user, page=self)

    def render(self, size):
        super().render(size)
