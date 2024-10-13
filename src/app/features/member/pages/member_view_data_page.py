import time
from app.app_context import AppContext
from app.constants import CITY, GENDER, ROLE
from app.context.member import Member
from app.context.user import User
from app.view.main_menu import MainMenu
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.info_box import InfoBox
from common.inter_act.components.screen import Screen
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class MemberViewDataPage(Page, metaclass=AutoWire):
    def __init__(self, engine: Engine, app_context: AppContext):
        from app.features.member.pages.manage_member import ManageMember

        self._member: Member = app_context.selected_member
        self._member_view_model = {
            "First Name": self._member.membership_id.decode(),
            "First Name": self._member.first_name.decode(),
            "Last Name": self._member.last_name.decode(),
            "Email address": self._member.email_address.decode(),
            "Phonenumber": self._member.phonenumber.decode(),
            "Gender": GENDER(self._member.gender),
            "Weight": self._member.weight.decode(),
            "Street & Housenumber": f'{self._member.street.decode()} {self._member.house_number.decode()}',
            "Zip code": self._member.zip_code.decode(),
            "City": CITY(self._member.city),
            "Registration Date": self._member.registration_date.decode()
        }
        super().__init__(engine=engine)
        self.options.update({
            'z': ManageMember,
            'm': MainMenu
        })

    def render_header(self, size):
        return TextBox.get_component(size, 2, f'Managing member {self._member.membership_id.decode()}').refresh()

    def render_body(self, size):
        screen = Screen([], size, 3, 1)
        InfoBox.get_component(size, '', 8, self._member_view_model).refresh()
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
