import time
from app.app_context import AppContext
from app.constants import ROLE
from app.context.user import User
from app.features.member.pages.member_delete_page import MemberDeletePage
from app.features.member.pages.member_update_city_page import MemberUpdateCityPage
from app.features.member.pages.member_update_firstname_page import MemberUpdateFirstnamePage
from app.features.member.pages.member_update_gender_page import MemberUpdateGenderPage
from app.features.member.pages.member_update_house_number_page import MemberUpdateHouseNumberPage
from app.features.member.pages.member_update_lastname_page import MemberUpdateLastnamePage
from app.features.member.pages.member_update_street_page import MemberUpdateStreetPage
from app.features.member.pages.member_update_weight_page import MemberUpdateWeightPage
from app.features.member.pages.member_update_zip_code_page import MemberUpdateZipCodePage
from app.features.member.pages.member_view_data_page import MemberViewDataPage
from app.features.member.pages.member_update_email_address import MemberUpdateEmailAddress
from app.features.member.pages.member_update_phonenumber_page import MemberUpdatePhonenumberPage
from app.view.main_menu import MainMenu
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.info_box import InfoBox
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class ManageMember(Page, metaclass=AutoWire):
    def __init__(self, engine: Engine, app_context: AppContext):
        super().__init__(engine=engine)
        self._member = app_context.selected_member
        self._app_context = app_context
        self.options.update({
            '1': MemberViewDataPage,
            '2': MemberUpdateFirstnamePage,
            '3': MemberUpdateLastnamePage,
            '4': MemberUpdateGenderPage,
            '5': MemberUpdateWeightPage,
            '6': MemberUpdateStreetPage,
            '7': MemberUpdateHouseNumberPage,
            '8': MemberUpdateZipCodePage,
            '9': MemberUpdateCityPage,
            '10': MemberUpdateEmailAddress,
            '11': MemberUpdatePhonenumberPage,
            '12': MemberDeletePage,
            'm': MainMenu
        })

        self.role_permissions = {
            "super_admin": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'm'],
            "admin": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'm'],
            "consultant": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', 'm']
        }

        self.options = {key: self.options[key] for key in self.role_permissions[ROLE(
            app_context.logged_in_user.role).decode()]}

    def render_header(self, size):
        return TextBox.get_component(size, 2, f'Managing member {self._member.membership_id.decode()}').refresh()

    def render_body(self, size):

        text_list_all = [' 👁️  - View member data ',
                         ' ✏️  - Change firstname ',
                         ' ✏️  - Change lastname ',
                         ' ✏️  - Change gender ',
                         ' ✏️  - Change weight ',
                         ' ✏️  - Change street ',
                         ' ✏️  - Change house number ',
                         ' ✏️  - Change zip code ',
                         ' ✏️  - Change City ',
                         ' ✏️  - Change email address ',
                         ' ✏️  - Change phonenumer ',
                         ' 🗑️  - Delete member ']

        text_list = [text_list_all[int(key) - 1] for key in self.role_permissions[ROLE(
            self._app_context.logged_in_user.role).decode()] if key.isdigit()]
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
