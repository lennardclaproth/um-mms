from app.app_context import AppContext
from app.constants import CITIES, GENDERS
from common.dependency_injection.auto_wire import AutoWire
from common.logging.logger import LoggerInterface
from common.validation.rules import not_none_or_empty, validate_contains, validate_email_address, validate_greater_than, validate_length, validate_phonenumber, validate_zip_code
from common.validation.validator import Validator


class MemberValidator(Validator, metaclass=AutoWire):
    def __init__(self, logger: LoggerInterface, app_context: AppContext):
        super().__init__(logger=logger, app_context=app_context)

        self.add_rule(validate_phonenumber("phonenumber"))
        self.add_rule(validate_contains("city", CITIES))
        self.add_rule(validate_contains("gender", GENDERS))
        self.add_rule(validate_email_address("email_address"))
        self.add_rule(validate_length("first_name"))
        self.add_rule(validate_length("last_name"))
        self.add_rule(validate_zip_code("zip_code"))
        self.add_rule(validate_greater_than("weight", 1))
        self.add_rule(not_none_or_empty("street"))
        self.add_rule(not_none_or_empty("house_number"))
