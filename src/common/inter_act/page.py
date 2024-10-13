from abc import ABC, abstractmethod

from common.inter_act.action import ActionInterface


class PageInterface(ABC):

    @abstractmethod
    def render_header(self, size):
        pass

    @abstractmethod
    def render_body(self, size):
        pass

    @abstractmethod
    def render_footer(self, size):
        pass

    @abstractmethod
    def perform_action(self):
        pass

    def render(self, size):
        self.render_header(size)
        self.render_footer(size)
        self.render_body(size)


class Page(PageInterface):

    _action: ActionInterface = None

    def __init__(self, *args, engine: 'Engine'):

        if args and len(args) > 0 and args[0] is not None and isinstance(args[0], ActionInterface):
            self._action = args[0]
        self.options = {
            'q': 'q',
            'z': lambda: engine.view_stack.pop_value().__class__
        }

    def perform_action(self):
        pass
