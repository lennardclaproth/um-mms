from app.context.member import Member
from app.context.user import User
from common.mediator.cqrs import Command


class DeleteMemberCommand(Command):
    def __init__(self, member: Member):
        self.member = member
