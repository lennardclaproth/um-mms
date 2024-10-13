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


class UserPasswordValidator(Validator, metaclass=AutoWire):
    def __init__(self, logger: LoggerInterface, app_context: AppContext, sender: Sender):
        super().__init__(logger=logger, app_context=app_context)

        self.add_rule(validate_password("password"))
