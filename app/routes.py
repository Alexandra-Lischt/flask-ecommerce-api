from apiflask import APIFlask
from flask import Blueprint

from app.modules.order.order_routes import order_bp
from app.modules.product.product_routes import product_bp
from app.modules.user.user_routes import user_bp


def register_v1_routes(app: APIFlask) -> None:
    v1_bp = Blueprint("v1", __name__, url_prefix="/api/v1")

    # O Blueprint do Flask aceita o aninhamento de submódulos nativamente
    v1_bp.register_blueprint(user_bp)
    v1_bp.register_blueprint(product_bp)
    v1_bp.register_blueprint(order_bp)

    # O APIFlask registra o blueprint agrupador sem reclamar de atributos ausentes
    app.register_blueprint(v1_bp)
