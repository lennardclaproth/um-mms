import time
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
from app.view.main_menu import MainMenu
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.info_box import InfoBox
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class UserViewDataPage(Page, metaclass=AutoWire):
    def __init__(self, engine: Engine, app_context: AppContext):
        from app.features.user.pages.manage_user import ManageUser

        self._user: User = app_context.selected_user
        self.user_view_model = {
            "Username": self._user.username.decode(),
            "First Name": self._user.first_name.decode(),
            "Last Name": self._user.last_name.decode(),
            "Role": ROLE(self._user.role).decode(),
            "Registration Date": self._user.registration_date.decode()
        }
        super().__init__(engine=engine)
        self.options.update({
            'z': ManageUser,
            'm': MainMenu
        })

    def render_header(self, size):
        return TextBox.get_component(size, 2, f'Managing user {self._user.username.decode()}').refresh()

    def render_body(self, size):
        screen = Screen([], size, 3, 1)
        InfoBox.get_component(size, '', 8, self.user_view_model).refresh()
        time.sleep(0.1)
        self.selected_option = screen.run()
        # return Text.get_component(text, size)

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit UM-MMS 🛑'
        TextBox.get_component(size, 10, text, size[0]-3).refresh()

    def perform_action(self):
        return self.options.get(self.selected_option)

    def render(self, size):
        self.render_header(size)
        self.render_footer(size)
        self.render_body(size)
