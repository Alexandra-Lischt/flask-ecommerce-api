# Arquivo: app/tests/modules/user/conftest.py

import pytest

from app.modules.user.user_interfaces import AbstractUserRepository
from app.modules.user.user_model import User


class MockUserRepository(AbstractUserRepository):
    def __init__(self) -> None:
        self.users: list[User] = []
        self.save_called = False

    def get_by_email(self, email: str) -> User | None:
        return next((user for user in self.users if user.email == email), None)

    def save(self, user: User) -> None:
        self.users.append(user)
        self.save_called = True


@pytest.fixture
def mock_user_repo():
    """Esta fixture estarÃ¡ disponÃ­vel apenas para os testes deste subdiretÃ³rio."""
    return MockUserRepository()
