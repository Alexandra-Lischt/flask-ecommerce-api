import uuid
from typing import Literal

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import TimestampMixin, UUIDIDMixin
from app.extensions import Model

OrderStatusType = Literal["pago", "cancelado", "pendente", "em_processamento"]


class OrderStatus:
    PENDENTE: OrderStatusType = "pendente"
    EM_PROCESSAMENTO: OrderStatusType = "em_processamento"
    PAGO: OrderStatusType = "pago"
    CANCELADO: OrderStatusType = "cancelado"


class OrderModel(Model, TimestampMixin, UUIDIDMixin):
    __tablename__ = "orders"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[OrderStatusType] = mapped_column(
        String(20), default=OrderStatus.PENDENTE, nullable=False
    )
    total_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    items: Mapped[list["OrderProductModel"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderProductModel(Model, TimestampMixin, UUIDIDMixin):
    """Tabela de associação (Pivot) entre Pedidos e Produtos com colunas de estado."""

    __tablename__ = "order_products"

    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_purchase: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped["OrderModel"] = relationship(back_populates="items")
