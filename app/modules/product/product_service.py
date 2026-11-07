from decimal import Decimal
from typing import Any

from apiflask import HTTPError

from app.extensions import db
from app.modules.product.product_interfaces import AbstractProductRepository
from app.modules.product.product_model import Product


class ProductService:
    def __init__(self, product_repo: AbstractProductRepository):
        self.product_repo = product_repo

    def list_products(self) -> list[Product]:
        return self.product_repo.list_all()

    def get_product(self, product_id: int) -> Product:
        product = self.product_repo.get_by_id(product_id)
        if product is None:
            raise HTTPError(404, message="Produto não encontrado.")
        return product

    def create_product(self, data: dict[str, Any]) -> Product:
        product = Product(
            name=data["name"],
            price=Decimal(str(data["price"])),
            stock=data["stock"],
            category=data["category"],
            description=data.get("description"),
        )
        return self._save(product)

    def update_product(self, product_id: int, data: dict[str, Any]) -> Product:
        product = self.get_product(product_id)
        product.name = data["name"]
        product.price = Decimal(str(data["price"]))
        product.stock = data["stock"]
        return self._save(product)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        try:
            self.product_repo.delete(product)
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            raise HTTPError(500, message="Erro ao excluir produto.") from exc

    def _save(self, product: Product) -> Product:
        try:
            self.product_repo.save(product)
            db.session.commit()
            return product
        except Exception as exc:
            db.session.rollback()
            raise HTTPError(500, message="Erro ao salvar produto.") from exc
