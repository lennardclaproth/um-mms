from typing import List
from app.app_context import AppContext
from app.constants import ROLES
from app.context.user import User
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.mediator.sender import Sender
from common.validation.rules import not_none_or_empty, validate_contains, validate_password, validate_username
from common.validation.validator import Validator


class UpdateUserValidator(Validator, metaclass=AutoWire):
    def __init__(self, logger: LoggerInterface, app_context: AppContext, sender: Sender):
        super().__init__(logger=logger, app_context=app_context)
        users: List[User] = sender.send(GetAllUsersQuery())
        usernames = []
        if users is not None:
            usernames = [user.username for user in users]

        self.add_rule(validate_username("username", usernames))
        self.add_rule(not_none_or_empty("first_name"))
        self.add_rule(not_none_or_empty("last_name"))
        self.add_rule(validate_contains("role", ROLES))
