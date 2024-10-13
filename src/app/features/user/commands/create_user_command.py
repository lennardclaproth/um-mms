from app.context.user import User
from common.mediator.cqrs import Command

class CreateUserCommand(Command):
    def __init__(self, user: User):
        self.user = user
