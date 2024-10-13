from app.features.member.actions.create_member_action import CreateMemberAction
from app.context.member import Member
from app.view.error_page import ErrorPage
from app.view.success_page import SuccessPage
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.input import Input
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class RegisterMemberPage(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine):
        self._action = engine.registry.get_action(CreateMemberAction)
        self.member = Member
        super().__init__(engine=engine)
        self.options.update({
            '1': SuccessPage,
            '2': ErrorPage
        })

    def render_header(self, size):
        text = 'Processing request please wait... 🔨'
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        self.member.first_name = Input.get_component("Please enter a first name", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.member.last_name = Input.get_component("Please enter a last name", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.member.gender = Input.get_component("Please enter the gender: \n1 for Male, \n2 for Female, \n3 for Other", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 4})
        self.member.weight = Input.get_component("Please enter the weight", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.member.phonenumber = Input.get_component("Please enter the phonenumber from +316 onwards", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.member.email_address = Input.get_component("Please enter the email adress", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.member.city = Input.get_component("Please enter the city, this can be one of the following. \n1. The Hague, \n2. Rotterdam, \n3. Leiden, \n4. Amsterdam \n5. Delft, \n6. Utrecht, \n7. Arnhem, \n8. Haarlem, \n9. Den Bosch, \n10. Zwolle", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 11})
        self.member.zip_code = Input.get_component("Please enter the zip code following the format DDDDXX", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.member.street = Input.get_component("Please enter the street name", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})
        self.member.house_number = Input.get_component("Please enter the house number", {
            'height': 15, 'width': 100, 'y': 3, 'x': 1, 'input_y': 1})

    def perform_action(self):
        return self._action.act(input=self.member, page=self)

    def render_footer(self, size):
        return super().render_footer(size)

    def render(self, size):
        self.render_body(size)
        self.render_header(size)
