from typing import List
from app.context.member import Member
from app.features.member.queries.find_member_query import FindMemberQuery
from app.features.member.queries.get_all_members_query import GetAllMembersQuery
from app.repositories.member_repository import MemberRepositoryInterface
from common.dependency_injection.auto_wire import AutoWire
from common.mediator.cqrs import QueryHandler


class GetAllMembersQueryHandler(QueryHandler[FindMemberQuery, List[Member]], metaclass=AutoWire):

    def __init__(self, member_repository: MemberRepositoryInterface):
        super().__init__()
        self._member_repository = member_repository

    def handle(self, query) -> List[Member]:
        return self._member_repository.find_member(query.search_string)
