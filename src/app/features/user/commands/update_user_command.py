from app.context.user import User
from common.mediator.cqrs import Command


class UpdateUserCommand(Command):
    def __init__(self, user: User, attribute: str):
        self.user = user
        self.attribute = attribute
