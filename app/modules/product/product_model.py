from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import TimestampMixin, UUIDIDMixin  # 💡 Importa o Mixin centralizado
from app.extensions import Model


class Product(
    Model, TimestampMixin, UUIDIDMixin
):  # 💡 Herança múltipla com o Mixin temporal
    __tablename__ = "products"

    # Restrição física no banco para impedir que o estoque fique negativo
    __table_args__ = (
        CheckConstraint("stock >= 0", name="check_product_stock_positive"),
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
