from app.context.user import User
from app.features.member.actions.create_member_action import CreateMemberAction
from app.context.member import Member
from app.features.user.actions.create_user_action import CreateUserAction
from app.view.error_page import ErrorPage
from app.view.success_page import SuccessPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.input import Input
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class RegisterUserPage(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine):
        self._action = engine.registry.get_action(CreateUserAction)
        self.user = User
        super().__init__(engine=engine)
        self.options.update({
            '1': SuccessPage,
            '2': ErrorPage
        })

    def render_header(self, size):
        text = 'Processing request please wait... 🔨'
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        special_characters = r'~!@#$%&_-+=`|\(){}[]:;\'<>,.?/'
        self.user.first_name = Input.get_component("Please enter a first name", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.user.last_name = Input.get_component("Please enter a last name", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.user.role = Input.get_component("Please enter the role: \n1 for Consultant, \n2 for Admin", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 3})
        self.user.username = Input.get_component("Please enter the username \n must be unique, at least 8 characters\n no longer than 10 characters\n must start with a letter or underscore\n can contain \n  letters (a-z), numbers (0-9), \n  underscores (_), apostrophes ('), and periods (.)\n no distinction between uppercase and lowercase", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 8})
        self.user.password = Input.get_component(f"Please enter the password, \n at least 12 characters and no more than 30 \n lower case allowed \n upper case allowed\n numbers (0-9) allowed\n allowed special characters: {special_characters}\n at least one uppercase, one lower case, one digit and one special character", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 7})

    def perform_action(self):
        return self._action.act(input=self.user, page=self)

    def render_footer(self, size):
        return super().render_footer(size)

    def render(self, size):
        self.render_body(size)
        self.render_header(size)
