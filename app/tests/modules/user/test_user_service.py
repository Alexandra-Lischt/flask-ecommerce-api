from unittest.mock import patch

import pytest
from apiflask import HTTPError

from app.modules.user.user_model import User
from app.modules.user.user_service import UserService


@patch("app.modules.user.user_service.db.session")
def test_create_user_com_sucesso(mock_session, mock_user_repo):
    service = UserService(user_repo=mock_user_repo)
    payload = {
        "name": "Gabriel Siqueira",
        "email": "gabriel@email.com",
        "password": "senha_segura_123",
    }

    novo_usuario = service.create_user(payload)

    assert novo_usuario.name == "Gabriel Siqueira"
    assert mock_user_repo.save_called is True
    mock_session.commit.assert_called_once()


@patch("app.modules.user.user_service.db.session")
def test_deve_impedir_cadastro_com_email_duplicado(mock_session, mock_user_repo):
    service = UserService(user_repo=mock_user_repo)
    mock_user_repo.users.append(
        User(name="Antigo", email="duplicado@email.com", password_hash="hash")
    )

    payload = {"name": "Novo", "email": "duplicado@email.com", "password": "123"}

    with pytest.raises(HTTPError) as exc_info:
        service.create_user(payload)

    assert exc_info.value.status_code == 400
    assert mock_user_repo.save_called is False
