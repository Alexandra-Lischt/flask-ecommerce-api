from decimal import Decimal
from typing import Any
from uuid import UUID

from apiflask import HTTPError
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.modules.order.order_interfaces import AbstractOrderRepository
from app.modules.order.order_model import OrderModel, OrderProductModel, OrderStatus
from app.modules.product.product_interfaces import AbstractProductRepository
from app.modules.user.user_interfaces import AbstractUserRepository


class OrderService:
    def __init__(
        self,
        order_repo: AbstractOrderRepository,
        product_repo: AbstractProductRepository,
        user_repo: AbstractUserRepository,
    ) -> None:
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.user_repo = user_repo

    def list_orders(self) -> list[OrderModel]:
        return self.order_repo.list_all()

    def create_order(self, payload: dict[str, Any]) -> OrderModel:
        try:
            if self.user_repo.get_by_id(payload["user_id"]) is None:
                raise HTTPError(404, message="Usuário não encontrado.")
            quantities: dict[UUID, int] = {}
            for item in payload["items"]:
                pid = item["product_id"]
                quantities[pid] = quantities.get(pid, 0) + item["quantity"]
            products = {}
            for pid in sorted(quantities):
                product = self.product_repo.get_by_id(pid)
                if product is None:
                    raise HTTPError(404, message="Produto não encontrado.")
                products[pid] = product
            order = OrderModel(
                user_id=payload["user_id"], status=OrderStatus.PENDENTE, total_price=0.0
            )
            total = Decimal("0")
            for pid in sorted(quantities):
                quantity = quantities[pid]
                price = Decimal(str(products[pid].price))
                if not self.product_repo.reserve_stock(pid, quantity):
                    raise HTTPError(409, message="Estoque insuficiente.")
                order.items.append(
                    OrderProductModel(
                        product_id=pid,
                        quantity=quantity,
                        price_at_purchase=float(price),
                    )
                )
                total += price * quantity
            order.total_price = float(total)
            self.order_repo.save(order)
            db.session.commit()
            return order
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise HTTPError(500, message="Erro ao criar pedido.") from exc
        except Exception:
            db.session.rollback()
            raise
