import importlib
import inspect
import pkgutil

from common.inter_act.page import Page, PageInterface
from common.inter_act.action import ActionInterface


class Registry:
    def __init__(self):
        self._pages = {}
        self._actions = {}

    def register(self, implementation):
        if issubclass(implementation, PageInterface):
            # page_type = self._get_generic_type(
            #     implementation, PageInterface)
            self._pages[implementation] = implementation
        elif issubclass(implementation, ActionInterface):
            # action_type = self._get_generic_type(implementation, ActionInterface)
            self._actions[implementation] = implementation

    # def _get_generic_type(self, implementation, base_class):
    #     test2 = implementation
    #     test = base_class
    #     for base in implementation.__orig_bases__:
    #         if getattr(base, "__origin__", None) is base_class:
    #             return base.__args__[0]
    #     raise ValueError(
    #         f"Could not determine generic type for {implementation}")

    def get_page(self, page_type):
        page = self._pages.get(page_type)
        if page is None:
            raise ValueError(
                f"Could not find page {page} in registry"
            )
        return page()

    def get_action(self, action_type):
        action_class = self._actions.get(action_type)
        if action_class is None:
            raise ValueError(
                f"Could not find action {action_type} in registry")
        return action_class()

    def scan_and_register(self, package):
        for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            print(f"Inspecting module: {module_name}")
            module = importlib.import_module(module_name)
            classes = inspect.getmembers(module, inspect.isclass)
            if not classes:
                print(f"No classes found in module: {module_name}")
            for name, obj in classes:
                if issubclass(obj, PageInterface) and obj is not PageInterface and obj is not Page:
                    print(f"Registering pages: {name}")
                    self.register(obj)
                elif issubclass(obj, ActionInterface) and obj is not ActionInterface:
                    print(f"Registering actions: {name}")
                    self.register(obj)
