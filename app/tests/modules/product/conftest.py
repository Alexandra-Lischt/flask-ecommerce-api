import uuid

import pytest

from app.modules.product.product_model import Product


class MemoryProductRepository:
    """Repositório em memória para isolamento de testes unitários do Produto."""

    def __init__(self) -> None:
        self.products: dict[uuid.UUID, Product] = {}

    def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        return self.products.get(product_id)

    def save(self, product: Product) -> None:
        # Se o modelo não tiver um UUID injetado pelo mixin, gera localmente
        if getattr(product, "id", None) is None:
            product.id = uuid.uuid4()
        self.products[product.id] = product

    def delete(self, product: Product) -> None:
        if getattr(product, "id", None) in self.products:
            self.products.pop(product.id)

    def list_all(self) -> list[Product]:
        return list(self.products.values())


@pytest.fixture
def memory_product_repo() -> MemoryProductRepository:
    """Fixture que fornece a instância limpa do repositório mockado."""
    return MemoryProductRepository()
