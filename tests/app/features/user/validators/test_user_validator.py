import pytest
from unittest.mock import Mock, MagicMock
from app.features.user.queries.get_all_users_query import GetAllUsersQuery
from app.features.user.validators.user_validator import UserValidator
from app.constants import ROLES
from app.context.user import User
from common.dependency_injection.auto_wire import AutoWire
from datetime import datetime


class TestUserValidator:
    """Test suite for the UserValidator class."""

    @pytest.fixture
    def mock_logger(self):
        """Fixture to create a mock logger."""
        return MagicMock()

    @pytest.fixture
    def mock_app_context(self):
        """Fixture to create a mock app context."""
        return MagicMock()

    @pytest.fixture
    def mock_sender(self):
        """Fixture to create a mock sender."""
        return MagicMock()

    @pytest.fixture
    def mock_users(self):
        """Fixture to create a list of mock users with all required attributes."""
        user1 = User(
            id=1,
            username="testuser1",
            password="Password123",
            first_name="John",
            last_name="Doe",
            role='consultant',  # Assume ROLES[0] is a valid role
            registration_date=datetime.now()
        )
        user2 = User(
            id=2,
            username="testuser2",
            password="Password456",
            first_name="Jane",
            last_name="Doe",
            role='consultant',  # Assume ROLES[1] is another valid role
            registration_date=datetime.now()
        )
        return [user1, user2]

    @pytest.fixture
    def setup_validator(self, mock_logger, mock_app_context, mock_sender, mock_users):
        """Fixture to set up UserValidator with mocked dependencies."""
        mock_sender.send.return_value = mock_users

        # Mock the AutoWire container to avoid the ValueError
        AutoWire.container = MagicMock()

        # Now instantiate the UserValidator with mocked dependencies
        return UserValidator(logger=mock_logger, app_context=mock_app_context, sender=mock_sender)

    def test_user_validator_validation_passes(self, setup_validator):
        """Test that validation passes for valid input."""
        validator = setup_validator

        # Create a mock user object with valid data
        valid_user = Mock()
        valid_user.username = "newuser1"
        valid_user.password = "ValidPassword123!"
        valid_user.first_name = "John"
        valid_user.last_name = "Doe"
        valid_user.role = ROLES[0]

        # Perform validation
        result = validator.validate(valid_user)

        # Assert that the validation passes
        assert result is True

    def test_user_validator_validation_fails_for_duplicate_username(self, setup_validator):
        """Test that validation fails when the username already exists."""
        validator = setup_validator

        # Create a mock user object with a duplicate username
        duplicate_user = Mock()
        duplicate_user.username = "testuser1"  # Same as in mock_users
        duplicate_user.password = "ValidPassword123"
        duplicate_user.first_name = "John"
        duplicate_user.last_name = "Doe"
        duplicate_user.role = ROLES[0]

        # Perform validation
        result = validator.validate(duplicate_user)

        # Assert that the validation fails
        assert result is False
        assert "Username 'testuser1' already exists" in validator._errors
