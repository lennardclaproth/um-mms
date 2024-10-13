import re

from common.validation.validator import NullByteValidationError, ValidationError, Validator


def ensure_str(input):
    if isinstance(input, bytes):
        return input.decode('utf-8')
    elif isinstance(input, str):
        return input
    else:
        raise ValueError("Input must be an instance of bytes or str")


def validate_phonenumber(param_name):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is invalid"))
                return False

            pattern = r"^\d{8}$"

            if re.fullmatch(pattern, value) is not None:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} is not in correct format"))
            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_smaller_than(param_name, threshold):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False

            value = float(value)

            if value < threshold:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} should not be bigger than {threshold}, value: {value}"))
            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_greater_than(param_name, threshold):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False

            value = float(value)

            if value > threshold:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} should not be smaller than {threshold}, value: {value}"))

            return False

        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def not_none_or_empty(param_name):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))

            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False

            if getattr(obj, param_name) is not None or value != "":
                return True

            validator._errors.append(ValidationError(
                f"{param_name} should not be None or empty"))
            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def min_length(param_name, min_len):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False

            if value is not None or len(value) > min_len:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} should be at least {min_len} characters long, value: {value}"))
            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def max_length(param_name, max_len):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                raise NullByteValidationError(f"{param_name} is not valid")

            if value is not None or len(value) < max_len:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} should be no more than {max_len} characters long, value: {value}"))

            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_contains(param_name, list):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))

            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False

            if int(value) <= len(list) and int(value) != 0:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} is not valid, input {value} is not a valid input"))

            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_length(param_name, min_len=1):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False

            if len(value) > min_len:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} is not valid, value: {value} is longer than {min_len}"))

            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_zip_code(param_name):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False
            pattern = r"^\d{4}[A-Z]{2}$"
            if re.fullmatch(pattern, value) is not None:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} is not valid, value: {value} does not follow DDDDXX format."))

            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_email_address(param_name):
    def rule(validator: Validator, obj):
        try:
            value = ensure_str(getattr(obj, param_name))
            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

            if re.fullmatch(pattern, value) is not None:
                return True

            validator._errors.append(ValidationError(
                f"{param_name} is not valid, value: {value} does not follow mail@mail.com format"))
            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_username(param_name, existing_usernames):
    def rule(validator: Validator, obj):
        try:
            # INFO: important this should be incremented for every check in this function
            validation_count = 4

            value = ensure_str(getattr(obj, param_name)).lower()

            if len(value) < 8 or len(value) > 10:
                validator._errors.append(ValidationError(
                    f"{param_name} must be between 8 and 10 characters long, value: {value}"))
                return False
            else:
                validation_count = validation_count - 1

            if not re.match(r'^[a-zA-Z_]', value):
                validator._errors.append(ValidationError(
                    f"{param_name} must start with a letter or underscore, value: {value}"))
                return False
            else:
                validation_count = validation_count - 1

            if not re.match(r'^[a-zA-Z0-9_.\'-]*$', value):
                validator._errors.append(ValidationError(
                    f"{param_name} contains invalid characters, value: {value}"))
                return False
            else:
                validation_count = validation_count - 1

            for username_byte_string in existing_usernames:
                username = ensure_str(username_byte_string)
                if username == value:
                    validator._errors.append(ValidationError(
                        f"{param_name} already exists, value: {value}"))
                    return False

            validation_count = validation_count - 1

            if validation_count == 0:
                return True

            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule


def validate_password(param_name):
    def rule(validator: Validator, obj):
        try:
            validation_count = 7

            value = ensure_str(getattr(obj, param_name))
            # INFO: important this should be incremented for every check in this function

            if '\x00' in value:
                validator._errors.append(
                    NullByteValidationError(f"{param_name} is not valid"))
                return False
            else:
                validation_count = validation_count - 1

            if len(value) < 12 or len(value) > 30:
                validator._errors.append(ValidationError(
                    f"{param_name} must be between 12 and 30 characters long"))
                return False
            else:
                validation_count = validation_count - 1

            if not re.search(r'[a-z]', value):
                validator._errors.append(ValidationError(
                    f"{param_name} must contain at least one lowercase letter"))
                return False
            else:
                validation_count = validation_count - 1

            if not re.search(r'[A-Z]', value):
                validator._errors.append(ValidationError(
                    f"{param_name} must contain at least one uppercase letter"))
                return False
            else:
                validation_count = validation_count - 1

            if not re.search(r'\d', value):
                validator._errors.append(ValidationError(
                    f"{param_name} must contain at least one digit"))
                return False
            else:
                validation_count = validation_count - 1

            if not re.search(r'[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/]', value):
                validator._errors.append(ValidationError(
                    f"{param_name} must contain at least one special character"))
                return False
            else:
                validation_count = validation_count - 1

            if not re.match(r'^[a-zA-Z0-9~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/]*$', value):
                validator._errors.append(ValidationError(
                    f"{param_name} contains invalid characters"))
                return False
            else:
                validation_count = validation_count - 1

            if validation_count == 0:
                return True

            return False
        except ValueError:
            validator._errors.append(
                ValidationError(f"{param_name} is not valid"))
            return False
    return rule
