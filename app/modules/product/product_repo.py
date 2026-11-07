from uuid import UUID

from app.extensions import db
from app.modules.product.product_interfaces import AbstractProductRepository
from app.modules.product.product_model import Product


class ProductRepository(AbstractProductRepository):
    def get_by_id(self, product_id: int | UUID) -> Product | None:
        return db.session.get(Product, product_id)

    def save(self, product: Product) -> None:
        db.session.add(product)

    def delete(self, product: Product) -> None:
        db.session.delete(product)

    def list_all(self) -> list[Product]:
        return list(db.session.scalars(db.select(Product)).all())

    def reserve_stock(self, product_id: UUID, quantity: int) -> bool:
        result = db.session.execute(
            db.update(Product)
            .where(Product.id == product_id, Product.stock >= quantity)
            .values(stock=Product.stock - quantity)
        )
        return result.rowcount == 1
