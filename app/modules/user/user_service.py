from apiflask import HTTPError
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.modules.user.user_interfaces import AbstractUserRepository
from app.modules.user.user_model import User


class UserService:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
    ) -> None:
        self.user_repo = user_repo

    def create_user(self, data: dict[str, str]) -> User:
        email = data["email"]
        existing_user = self.user_repo.get_by_email(email)

        if existing_user:
            raise HTTPError(400, message="Este e-mail já está cadastrado.")

        new_user = User(
            name=data["name"],
            email=email,
            role=data.get("role"),
            password_hash=self.hash_password(data["password"]),
        )

        try:
            self.user_repo.save(new_user)
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            raise HTTPError(
                500, message="Erro interno ao salvar os dados no servidor."
            ) from exc

        return new_user

    @staticmethod
    def hash_password(password: str) -> str:
        if not password:
            raise HTTPError(400, message="A senha é obrigatória.")
        return generate_password_hash(password)
