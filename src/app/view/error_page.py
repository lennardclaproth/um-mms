from app.app_context import AppContext
from common.dependency_injection.auto_wire import AutoWire
from common.inter_act.components.text import Text
from common.inter_act.components.textbox import TextBox
from common.inter_act.engine import Engine
from common.inter_act.page import Page


class ErrorPage(Page, metaclass=AutoWire):

    def __init__(self, engine: Engine, app_context: AppContext):
        from app.view.main_menu import MainMenu

        self._app_context = app_context
        self._engine = engine
        super().__init__(engine=engine)
        self.options.update({
            "m": MainMenu
        })

    def render_header(self, size):
        TextBox.get_component(size, 3, 'An error occured 😥').refresh()

    def render_body(self, size):
        error_string = str(self._app_context.error)
        Text.get_component(error_string, size).refresh()

    def render_footer(self, size):
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑'
        padding = 10
        text = 'm: back to main menu 🏡 \t q: quit the GoodChain 🛑 \t z: redo previous action 👈'
        padding = 16
        TextBox.get_component(size, padding, text, size[0]-3).refresh()

    def perform_action(self):
        option = self._engine.screen.getch()
        options_chr = chr(option)
        if options_chr == 'z':
            return self.options.get(options_chr)()
        return self.options.get(chr(option))

    def render(self, size):
        super().render(size)
