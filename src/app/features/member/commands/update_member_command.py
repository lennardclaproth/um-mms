from app.context.member import Member
from app.context.user import User
from common.mediator.cqrs import Command


class UpdateMemberCommand(Command):
    def __init__(self, member: Member, attribute: str):
        self.member = member
        self.attribute = attribute
