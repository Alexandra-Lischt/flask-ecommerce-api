# Arquivo: app/tests/modules/user/test_user_integration.py
from app.extensions import db
from app.modules.user.user_model import User


def test_integracao_fluxo_completo_cadastro_usuario(client, app):
    # 1. Arrange: Payload enviado pelo cliente da API
    payload = {
        "name": "Alan Turing",
        "email": "alan@enigma.com",
        "password": "senha_criptografada_123",
    }

    # 2. Act: Realiza o disparo HTTP POST real na rota da API
    response = client.post("/api/v1/users/", json=payload)
    response_json = response.get_json()

    # 3. Assert: Valida a resposta HTTP retornada pela rota
    assert response.status_code == 201
    assert response_json["name"] == "Alan Turing"
    assert response_json["email"] == "alan@enigma.com"
    assert "id" in response_json

    with app.app_context():
        usuario_no_banco = db.session.scalar(
            db.select(User).filter_by(email="alan@enigma.com")
        )

        assert usuario_no_banco is not None
        assert usuario_no_banco.name == "Alan Turing"
        assert usuario_no_banco.password_hash != "senha_criptografada_123"


def test_integracao_deve_rejeitar_email_duplicado_no_banco_real(client, app):
    # 1. Arrange: Força a inserção prévia de um usuário direto no banco de dados real
    with app.app_context():
        usuario_existente = User(
            name="Grace Hopper", email="grace@cobol.com", password_hash="hash_qualquer"
        )
        db.session.add(usuario_existente)
        db.session.commit()

    # Payload com o mesmo e-mail que acabamos de salvar
    payload_duplicado = {
        "name": "Outra Grace",
        "email": "grace@cobol.com",
        "password": "outra_senha_123",
    }

    # 2. Act: Dispara a requisição HTTP na rota
    response = client.post("/api/v1/users/", json=payload_duplicado)
    response_json = response.get_json()

    # 3. Assert: Valida se a rota interceptou a duplicação usando o banco de dados
    assert response.status_code == 400
    assert response_json["status"] == "error"
    assert "Este e-mail já está cadastrado." in response_json["message"]
