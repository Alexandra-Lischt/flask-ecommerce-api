# Arquivo: app/tests/conftest.py
import pytest

from app import create_app
from app.extensions import db


@pytest.fixture(scope="session")
def app():
    """Cria e configura uma instância do app Flask para a suíte de testes."""
    app = create_app()

    # Força o uso do SQLite em memória para isolar completamente os dados do teste
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    # Cria as tabelas físicas no banco de dados temporário antes de rodar os testes
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Retorna um cliente HTTP do Flask limpo."""
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_database(app):
    """Limpa os dados das tabelas após a execução de CADA teste individual."""
    with app.app_context():
        yield
        # Faz rollback para evitar sessões presas e limpa os registros
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
