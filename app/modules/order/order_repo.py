from app.extensions import db
from app.modules.order.order_interfaces import AbstractOrderRepository
from app.modules.order.order_model import OrderModel


class OrderRepository(AbstractOrderRepository):
    def save(self, order: OrderModel) -> None:
        db.session.add(order)

    def get_by_id(self, order_id: int) -> OrderModel | None:
        return db.session.get(OrderModel, order_id)

    def get_by_user(self, user_id: int) -> list[OrderModel]:
        return db.session.query(OrderModel).filter_by(user_id=user_id).all()

    def list_all(self) -> list[OrderModel]:
        return list(db.session.scalars(db.select(OrderModel)).all())
