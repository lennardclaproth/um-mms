import time
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
from app.features.user.pages.user_delete_page import UserDeletePage
from app.features.user.pages.user_reset_password_page import UserResetPasswordPage
from app.features.user.pages.user_update_firstname_page import UserUpdateFirstnamePage
from app.features.user.pages.user_update_lastname_page import UserUpdateLastnamePage
from app.features.user.pages.user_view_data_page import UserViewDataPage
from app.view.main_menu import MainMenu
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.info_box import InfoBox
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class ManageUser(Page, metaclass=AutoWire):
    def __init__(self, engine: Engine, app_context: AppContext):
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
            '1': UserViewDataPage,
            '2': UserUpdateFirstnamePage,
            '3': UserUpdateLastnamePage,
            '4': UserResetPasswordPage,
            '5': UserDeletePage,
            'm': MainMenu
        })

    def render_header(self, size):
        return TextBox.get_component(size, 2, f'Managing user {self._user.username.decode()}').refresh()

    def render_body(self, size):

        text_list = [' 👁️  - View user data',
                     ' ✏️  - Change firstname ',
                     ' ✏️  - Change lastname ',
                     ' ↩️  - Reset password ',
                     ' 🗑️  - Delete user ',]
        screen = Screen(text_list, size, 3)
        time.sleep(0.2)
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
