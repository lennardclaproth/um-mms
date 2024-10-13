from common.mediator.cqrs import Command, CommandHandler, Query, QueryHandler
from common.mediator.registry import Registry
import app


class Sender:
    def __init__(self):
        self.registry = Registry()
        self.registry.scan_and_register(app)

    def send(self, request):
        if isinstance(request, Command):
            handler_class = self.registry.get_command_handler(type(request))
            if handler_class:
                handler = handler_class()
                handler.handle(request)
            else:
                raise ValueError(
                    f"No handler found for command {type(request)}")
        elif isinstance(request, Query):
            handler_class = self.registry.get_query_handler(type(request))
            if handler_class:
                handler = handler_class()
                return handler.handle(request)
            else:
                raise ValueError(f"No handler found for query {type(request)}")
        else:
            raise ValueError("Unknown request type")
