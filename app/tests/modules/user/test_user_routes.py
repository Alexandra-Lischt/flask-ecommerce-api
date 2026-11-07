from datetime import UTC, datetime
from unittest.mock import patch

from app.modules.user.user_model import User


@patch("app.modules.user.user_routes.UserService.create_user")
def test_rota_create_user_com_payload_valido(mock_create_user, client):
    """Deve retornar 201 e o schema de resposta correto se o payload HTTP for válido"""

    # 1. Arrange: Configuramos o que o serviço falso deve retornar ao ser chamado
    user_falso = User(
        id=1,
        name="John Doe",
        email="john@example.com",
        password_hash="hash_seguro",
        created_at=datetime.now(UTC),
    )
    mock_create_user.return_value = user_falso

    payload_valido = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "senha_ultra_segura",
    }

    # 2. Act: Fazemos o disparo HTTP POST real na rota usando o cliente de teste
    response = client.post("/api/v1/users/", json=payload_valido)
    response_json = response.get_json()

    # 3. Assert: Validamos o comportamento do contrato HTTP do APIFlask
    assert response.status_code == 201
    assert response_json["name"] == "John Doe"
    assert response_json["email"] == "john@example.com"
    assert "id" in response_json
    assert "created_at" in response_json
    assert (
        "password" not in response_json
    )  # Garante que o UserResponseSchema filtrou e escondeu a senha

    # Confirma que a rota cumpriu seu papel e chamou o serviço correto
    mock_create_user.assert_called_once_with(payload_valido)


@patch("app.modules.user.user_routes.UserService.create_user")
def test_rota_create_user_deve_barrar_payload_invalido(mock_create_user, client):
    """Deve retornar erro de validação (400) se faltarem campos obrigatórios no JSON"""

    # 1. Arrange: Payload inválido de propósito (sem o campo obrigatório 'email')
    payload_invalido = {"name": "John Doe", "password": "senha_qualquer"}

    # 2. Act: Dispara o POST na API
    response = client.post("/api/v1/users/", json=payload_invalido)
    response_json = response.get_json()

    # 3. Assert: O APIFlask deve barrar a requisição baseado no UserCreateSchema
    # Como configuramos app.config['VALIDATION_ERROR_STATUS_CODE'] = 400
    assert response.status_code == 400

    assert response_json["status"] == "error"
    assert (
        "details" in response_json
    )  # Contém o mapeamento do erro informando que o e-mail faltou

    mock_create_user.assert_not_called()
