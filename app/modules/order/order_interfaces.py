from abc import ABC, abstractmethod

from app.modules.order.order_model import OrderModel


class AbstractOrderRepository(ABC):
    @abstractmethod
    def save(self, order: OrderModel) -> None:
        ...

    @abstractmethod
    def list_all(self) -> list[OrderModel]:
        ...
