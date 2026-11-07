from typing import Any

from apiflask import APIBlueprint

from app.modules.order.order_model import OrderModel
from app.modules.order.order_repo import OrderRepository
from app.modules.order.order_schema import OrderCreateSchema, OrderResponseSchema
from app.modules.order.order_service import OrderService
from app.modules.product.product_repo import ProductRepository
from app.modules.user.user_repo import UserRepository

order_bp = APIBlueprint("order", __name__, url_prefix="/orders", tag="Order")


def _service() -> OrderService:
    return OrderService(OrderRepository(), ProductRepository(), UserRepository())


@order_bp.get("/")
@order_bp.output(OrderResponseSchema(many=True))
def list_orders() -> list[OrderModel]:
    return _service().list_orders()


@order_bp.post("/")
@order_bp.input(OrderCreateSchema)
@order_bp.output(OrderResponseSchema, status_code=201)
def create_order(json_data: dict[str, Any]) -> OrderModel:
    return _service().create_order(json_data)
