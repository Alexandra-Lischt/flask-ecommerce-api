from abc import ABC, abstractmethod

from app.modules.user.user_model import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Busca um usuário no banco através do e-mail."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        """Busca um usuário no banco através do ID."""
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        """Adiciona a entidade instanciada no contexto da sessão."""
        pass
