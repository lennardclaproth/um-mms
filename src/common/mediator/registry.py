import importlib
import inspect
import pkgutil

from common.mediator.cqrs import CommandHandler, QueryHandler


class Registry:
    def __init__(self):
        self._command_handlers = {}
        self._query_handlers = {}

    def register(self, handler_class):
        if issubclass(handler_class, CommandHandler):
            command_type = self._get_generic_type(
                handler_class, CommandHandler)
            self._command_handlers[command_type] = handler_class
        elif issubclass(handler_class, QueryHandler):
            query_type = self._get_generic_type(handler_class, QueryHandler)
            self._query_handlers[query_type] = handler_class

    def _get_generic_type(self, handler_class, base_class):
        for base in handler_class.__orig_bases__:
            if getattr(base, "__origin__", None) is base_class:
                return base.__args__[0]
        raise ValueError(
            f"Could not determine generic type for {handler_class}")

    def get_command_handler(self, command_type):
        return self._command_handlers.get(command_type)

    def get_query_handler(self, query_type):
        return self._query_handlers.get(query_type)

    def scan_and_register(self, package):
        for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            print(f"Inspecting module: {module_name}")
            module = importlib.import_module(module_name)
            classes = inspect.getmembers(module, inspect.isclass)
            if not classes:
                print(f"No classes found in module: {module_name}")
            for name, obj in classes:
                if issubclass(obj, CommandHandler) and obj is not CommandHandler:
                    print(f"Registering command handler: {name}")
                    self.register(obj)
                elif issubclass(obj, QueryHandler) and obj is not QueryHandler:
                    print(f"Registering query handler: {name}")
                    self.register(obj)
