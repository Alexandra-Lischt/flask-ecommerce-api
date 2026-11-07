from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    """Classe base declarativa do SQLAlchemy para os modelos do ecossistema."""

    pass


db = SQLAlchemy(model_class=Model)
migrate = Migrate()


def init_db(app: Flask) -> None:
    """Inicializa as extensões vinculando-as ao ciclo de vida do app Flask atual."""
    db.init_app(app)
    migrate.init_app(app, db)
