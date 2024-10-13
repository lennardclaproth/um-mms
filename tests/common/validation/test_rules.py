# # Add the src directory to the Python path

from common.validation.rules import ensure_str

from common.validation.rules import validate_phonenumber
from common.validation.validator import NullByteValidationError, ValidationError, Validator

import pytest
from unittest.mock import Mock


@pytest.fixture
def setup_validator():
    logger = Mock()
    app_context = Mock()
    app_context.logged_in_user.username.decode.return_value = "test_user"
    return Validator(logger, app_context)


def test_valid_phonenumber(setup_validator):
    validator = setup_validator
    validator.add_rule(validate_phonenumber("phone_number"))
    obj = Mock()
    obj.phone_number = "12345678"
    result = validator.validate(obj)
    assert result is True


def test_invalid_phonenumber_format(setup_validator):
    validator = setup_validator
    validator.add_rule(validate_phonenumber("phone_number"))
    obj = Mock()
    obj.phone_number = "1234567"
    result = validator.validate(obj)
    assert result is False
    assert len(validator._errors) == 1
    assert "is not in correct format" in str(validator._errors[0])


def test_ensure_str_with_bytes():
    """Test that ensure_str decodes bytes to string."""
    input_data = b'hello'
    result = ensure_str(input_data)
    assert result == 'hello'
    assert isinstance(result, str)


def test_ensure_str_with_str():
    """Test that ensure_str returns the input when it is already a string."""
    input_data = 'hello'
    result = ensure_str(input_data)
    assert result == input_data
    assert isinstance(result, str)


def test_ensure_str_raises_value_error():
    """Test that ensure_str raises ValueError for non-bytes and non-str input."""
    input_data = 12345  # Invalid input (not str or bytes)

    with pytest.raises(ValueError, match="Input must be an instance of bytes or str"):
        ensure_str(input_data)
