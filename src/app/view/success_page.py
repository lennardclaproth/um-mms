from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.textbox import TextBox
from common.inter_act.components.text import Text
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class SuccessPage(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine):
        from app.view.main_menu import MainMenu

        self._engine = engine
        super().__init__(engine=engine)
        self.options.update({
            'm': MainMenu
        })

    def render_header(self, size):
        text = 'Succesfully handled your request 🎊'
        TextBox.get_component(size, 3, text).refresh()

    def render_body(self, size):
        text = 'Successfully handled your request.If you press m you will be automatically redirected to the main menu.'
        Text.get_component(text, size).refresh()

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit UM-MMS 🛑'
        TextBox.get_component(size, 10, text, size[0]-3).refresh()

    def perform_action(self):
        option = self._engine.screen.getch()
        return self.options.get(chr(option))

    def render(self, size):
        super().render(size)
