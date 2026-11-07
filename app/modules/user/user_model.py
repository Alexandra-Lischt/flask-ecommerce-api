from typing import Literal

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import TimestampMixin, UUIDIDMixin  # 💡 Importa o Mixin centralizado
from app.extensions import Model

RoleType = Literal["admin", "user"]


class Role:
    ADMIN: RoleType = "admin"
    USER: RoleType = "user"


class User(
    Model, TimestampMixin, UUIDIDMixin
):  # 💡 Herança do Mixin temporal aplicada aqui
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    role: Mapped[RoleType] = mapped_column(
        String(50), nullable=False, default=Role.USER
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
