from typing import Any

from apiflask import APIBlueprint

from app.modules.product.product_model import Product
from app.modules.product.product_repo import ProductRepository
from app.modules.product.product_schema import (
    ProductCreateSchema,
    ProductResponseSchema,
)
from app.modules.product.product_service import ProductService

product_bp = APIBlueprint("product", __name__, url_prefix="/products", tag="Product")


def _service() -> ProductService:
    return ProductService(ProductRepository())


@product_bp.get("/")
@product_bp.output(ProductResponseSchema(many=True))
def list_products() -> list[Product]:
    return _service().list_products()


@product_bp.get("/<int:product_id>")
@product_bp.output(ProductResponseSchema)
def get_product(product_id: int) -> Product:
    return _service().get_product(product_id)


@product_bp.post("/")
@product_bp.input(ProductCreateSchema)
@product_bp.output(ProductResponseSchema, status_code=201)
def create_product(json_data: dict[str, Any]) -> Product:
    return _service().create_product(json_data)


@product_bp.put("/<int:product_id>")
@product_bp.input(ProductCreateSchema)
@product_bp.output(ProductResponseSchema)
def update_product(product_id: int, json_data: dict[str, Any]) -> Product:
    return _service().update_product(product_id, json_data)


@product_bp.delete("/<int:product_id>")
def delete_product(product_id: int) -> tuple[str, int]:
    _service().delete_product(product_id)
    return "", 204
