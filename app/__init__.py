import os

from apiflask import APIFlask
from dotenv import load_dotenv

from app.extensions import init_db

load_dotenv()


def create_app() -> APIFlask:
    app = APIFlask(__name__, title="E-commerce API", version="1.0")

    # Configurações do Banco de Dados
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///project.db"
    )

    app.config["AUTO_VALIDATION_ERROR_RESPONSE"] = False

    # 1. Inicializa o banco de dados primeiro
    init_db(app)

    # 2. IMPORTAÇÃO LOCAL: Importe aqui dentro para evitar loops de importação
    from app.routes import register_v1_routes

    register_v1_routes(app)

    return app
