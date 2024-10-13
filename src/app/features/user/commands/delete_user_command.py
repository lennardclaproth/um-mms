from app.context.user import User
from common.mediator.cqrs import Command


class DeleteUserCommand(Command):
    def __init__(self, user: User):
        self.user = user
