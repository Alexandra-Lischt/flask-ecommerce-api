from app.extensions import db
from app.modules.user.user_interfaces import (
    AbstractUserRepository,
)
from app.modules.user.user_model import User


class UserRepository(AbstractUserRepository):
    def save(self, user: User) -> None:
        db.session.add(user)

    def get_by_email(self, email: str) -> User | None:
        return db.session.query(User).filter_by(email=email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return db.session.query(User).filter_by(id=user_id).first()
