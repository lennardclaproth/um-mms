from app.context.member import Member
from common.mediator.cqrs import Command


class CreateMemberCommand(Command):
    def __init__(self, member: Member):
        self.member = member
