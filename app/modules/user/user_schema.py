from apiflask.fields import DateTime, Integer, String
from apiflask.schemas import Schema
from marshmallow.validate import Email, Length


class UserCreateSchema(Schema):
    name = String(required=True, metadata={"description": "Nome completo do usuário"})
    email = String(
        required=True,
        metadata={"description": "E-mail válido do usuário"},
        validate=Email(),
    )
    role = String(
        required=True,
        metadata={"description": "Função do usuário (admin ou user)"},
        validate=Length(min=4, max=5),
    )
    password = String(
        required=True,
        metadata={"description": "Mínimo de 6 caracteres"},
        validate=Length(min=6),
        load_only=True,
    )


class UserResponseSchema(Schema):
    id = Integer(dump_only=True)
    name = String()
    email = String()
    role = String()
    created_at = DateTime()
