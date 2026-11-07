from typing import Any

from apiflask import APIBlueprint

from app.modules.user.user_model import User
from app.modules.user.user_repo import UserRepository
from app.modules.user.user_schema import UserCreateSchema, UserResponseSchema
from app.modules.user.user_service import (
    UserService,  # <-- Corrigido o caminho e o nome da classe
)

# Criação do Blueprint usando o padrão do APIFlask
user_bp = APIBlueprint("user", __name__, url_prefix="/users", tag="User")


def _service() -> UserService:
    return UserService(UserRepository())


@user_bp.post("/")
@user_bp.input(UserCreateSchema)
@user_bp.output(UserResponseSchema, status_code=201)
def create_user(json_data: dict[str, Any]) -> User:
    return _service().create_user(json_data)
