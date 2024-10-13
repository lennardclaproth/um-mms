from hashlib import sha256
from typing import List, Tuple
from app.context.unique_meal_db_context import UniqueMealDbContext
from app.context.member import Member
from common.dependency_injection.auto_wire import AutoWire
from abc import ABC, abstractmethod

from common.smart_db.context import DbContext


class MemberRepositoryInterface(ABC):

    @abstractmethod
    def create_member(self, member: Member):
        pass

    @abstractmethod
    def get_members(self):
        pass

    @abstractmethod
    def update_member(self, member: Member):
        pass

    @abstractmethod
    def delete_member(self, member: str):
        pass

    @abstractmethod
    def find_member(self, search_string: str):
        pass


class MemberRepository(MemberRepositoryInterface, metaclass=AutoWire):

    def __init__(self, context: DbContext):
        self._context: UniqueMealDbContext = context

    def create_member(self, member: Member):
        self._context.members.reset_query_builder()
        self._context.members.create(member)
        self._context.save_changes()
        return member

    def get_members(self):
        self._context.members.reset_query_builder()
        members = self._context.members.get_all()
        self._context.close_db()
        return members

    def update_member(self, member: Member, attribute: str):
        self._context.members.reset_query_builder()
        self._context.members.update(member, attribute_name=attribute)
        self._context.save_changes()

    def delete_member(self, member: Member):
        self._context.members.reset_query_builder()
        self._context.members.delete(member.id)
        self._context.save_changes()

    def find_member(self, search_string: str):
        self._context.members.reset_query_builder()
        search_fields = ["membership_id", "last_name", "first_name",
                         "email_address", "phonenumber", "zip_code", "street", "house_number"]
        result = self._context.members.search(
            search_fields, search_string).all()
        self._context.close_db()
        return result
