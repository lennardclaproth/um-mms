from hashlib import sha256
from typing import List, Tuple
from app.app_context import AppContext
from app.context.unique_meal_db_context import UniqueMealDbContext
from app.context.member import Member
from app.context.user import User
from common.cryptography.data_encoder import Encoder
from common.dependency_injection.auto_wire import AutoWire
from abc import ABC, abstractmethod

from common.smart_db.context import DbContext


class UserRepositoryInterface(ABC):

    @abstractmethod
    def create_user(self, user: User):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def update_user(self, user: User, attribute: str):
        pass

    @abstractmethod
    def delete_user(self, user: str):
        pass

    @abstractmethod
    def get_users_by_username(self, username: str):
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        pass


class UserRepository(UserRepositoryInterface, metaclass=AutoWire):

    def __init__(self, context: DbContext, encoder: Encoder, app_context: AppContext):
        self._context: UniqueMealDbContext = context
        self._encoder: Encoder = encoder
        self._app_context = app_context

    def create_user(self, user: User):
        self._context.users.reset_query_builder()
        self._context.users.create(user)
        self._context.save_changes()
        return user

    def get_users_by_username(self, username: str):
        self._context.users.reset_query_builder()
        users = self._context.users.where("username").equals(
            username).all()
        return users

    def get_user_by_username(self, username: str):
        self._context.users.reset_query_builder()
        user = self._context.users.where(
            "username").equals(username).first_or_none()
        self._context.close_db()
        return user

    def get_users(self):
        self._context.users.reset_query_builder()

        users = self._context.users.get_all()
        self._context.close_db()
        return users

    def update_user(self, user: User, attribute: str):
        self._context.users.reset_query_builder()
        self._context.users.update(user, attribute_name=attribute)
        self._context.save_changes()

    def delete_user(self, user: User):
        self._context.users.delete(user.id)
        self._context.save_changes()
