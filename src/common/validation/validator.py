from app.app_context import AppContext
from common.logging.logger import LoggerInterface


class ValidationError(Exception):
    pass


class NullByteValidationError(Exception):
    pass


class Validator:
    def __init__(self, logger: LoggerInterface, app_context: AppContext):
        self._rules = []
        self._errors = []
        self._is_suspicious_validation = False
        self.logger = logger
        self.app_context = app_context

    def add_rule(self, rule):
        self._rules.append(rule)
        return self

    def validate(self, obj):
        fail_safe = True
        self._errors = []

        for rule in self._rules:
            if rule(self, obj) == False:
                fail_safe = False

        if len(self._errors) == 0 and fail_safe == True:
            return True

        # for error in self._errors:
        #     self.logger.warning("Validation error occurred")
        #     if isinstance(error, NullByteValidationError):
        #         self._is_suspicious_validation = True
        #         self.logger.warning(
        #             "Attempted null byte attack",
        #             exception=error,
        #             actor=self.app_context.logged_in_user.username.decode(),
        #             action="Validating input",
        #             suspicious="Yes"
        #         )

        self.logger.warning("Validation error occurred, one or more validation errors occurred.",
                            exceptions = self._errors,
                            actor=self.app_context.logged_in_user.username.decode(),
                            action="Validating input")

        return False
