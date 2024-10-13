import curses
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
from common.logging.log import Log


class LoggingViewLogPage(Page, metaclass=AutoWire):
    def __init__(self, engine: Engine, app_context: AppContext):
        self._log: Log = app_context.selected_log
        self.log_view_model = {
            "Level": self._log.level,
            "message": self._log.message,
            "extra_info": self._log.kwargs,
        }
        super().__init__(engine=engine)
        self.options.update({
            'm': MainMenu
        })

    def render_header(self, size):
        return TextBox.get_component(size, 2, f'Viewing log').refresh()

    def render_body(self, size):
        screen = Screen([], size, 3, width=1)
        color = curses.COLOR_BLUE
        if self._log.level == "ERROR":
            color = curses.COLOR_RED
        elif self._log.level == "SUSPICIOUS":
            color = curses.COLOR_RED
        elif self._log.level == "WARNING":
            color = curses.COLOR_YELLOW
        InfoBox.get_component(
            size, '', 8, self.log_view_model, text_color=color).refresh()
        time.sleep(0.2)
        self.selected_option = screen.run()
        # return Text.get_component(text, size)

    def render_footer(self, size):
        text = ' m: back to main menu 🏡 \t q: quit UM-MMS 🛑 '
        TextBox.get_component(size, 10, text, size[0]-3).refresh()

    def perform_action(self):
        return self.options.get(self.selected_option)

    def render(self, size):
        self.render_header(size)
        self.render_footer(size)
        self.render_body(size)
