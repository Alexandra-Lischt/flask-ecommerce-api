from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.product.product_model import Product


class AbstractProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int | UUID) -> Product | None:
        ...

    @abstractmethod
    def save(self, product: Product) -> None:
        ...

    @abstractmethod
    def delete(self, product: Product) -> None:
        ...

    @abstractmethod
    def list_all(self) -> list[Product]:
        ...

    @abstractmethod
    def reserve_stock(self, product_id: UUID, quantity: int) -> bool:
        ...
