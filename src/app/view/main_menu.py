from app.features.member.pages.register_member_page import RegisterMemberPage
from app.features.user.pages.user_login_page import UserLoginPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class MainMenu(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine):
        super().__init__(engine=engine)
        self.options.update({
            '1': UserLoginPage
        })

    def render_header(self, size):
        return TextBox.get_component(size, 2, 'Welcome to the US-MMS').refresh()

    def render_body(self, size):
        text_list = [' 👤 - Log in ']
        screen = Screen(text_list, size, 3)
        self.selected_option = screen.run()
        # return Text.get_component(text, size)

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit UM-MMS 🛑'
        TextBox.get_component(size, 10, text, size[0]-3).refresh()

    def perform_action(self):
        if self.selected_option == 'm' or self.selected_option == 'q':
            return self.selected_option
        return self.options.get(self.selected_option)

    def render(self, size):
        super().render(size)
