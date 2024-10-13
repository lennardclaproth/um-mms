import time
from app.app_context import AppContext
from app.constants import ROLE
from app.features.logging.pages.logging_view_page import LoggingViewPage
from app.features.member.pages.member_find_page import MemberFindPage
from app.features.member.pages.register_member_page import RegisterMemberPage
from app.features.member.pages.view_members import ViewMembersPage
from app.features.user.pages.register_user_page import RegisterUserPage
from app.features.user.pages.user_create_backup_page import UserCreateBackupPage
from app.features.user.pages.user_restore_page import UserRestorePage
from app.features.user.pages.view_users import ViewUsersPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class UserMenu(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine, app_context: AppContext):
        super().__init__(engine=engine)
        self.options.update({
            '1': RegisterMemberPage,
            '2': ViewMembersPage,
            '3': MemberFindPage,
            '4': ViewUsersPage,
            '5': RegisterUserPage,
            '6': LoggingViewPage,
            '7': UserCreateBackupPage,
            '8': UserRestorePage
        })
        self._app_context = app_context

        self.role_permissions = {
            "super_admin": ['1', '2', '3', '4', '5', '6', '7', '8'],
            "admin": ['1', '2', '3', '4', '5', '6', '7', '8'],
            "consultant": ['1', '2', '3', '4']
        }

        self.options = {key: self.options[key] for key in self.role_permissions[ROLE(
            self._app_context.logged_in_user.role).decode()]}

    def render_header(self, size):
        return TextBox.get_component(size, 2, f'Welcome {self._app_context.logged_in_user.first_name.decode()} {self._app_context.logged_in_user.last_name.decode()}').refresh()

    def render_body(self, size):
        text_list_all = [' 📋 - Register new Member ',
                         ' 👥 - View Members',
                         ' 🔍 - Find Members',
                         ' 👥 - View Users ',
                         ' 📋 - Register new User ',
                         ' 📝 - View Logs ',
                         ' ⬇️  - Create backup ',
                         ' ⬆️  - Import from backup']

        text_list = [text_list_all[int(key) - 1] for key in self.role_permissions[ROLE(
            self._app_context.logged_in_user.role).decode()] if key.isdigit()]
        time.sleep(0.2)
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