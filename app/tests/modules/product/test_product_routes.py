from decimal import Decimal
from unittest.mock import patch

from app.modules.product.product_model import Product


@patch("app.modules.product.product_routes.ProductService.list_products")
def test_list_products(mock_list, client):
    mock_list.return_value = [
        Product(id=1, name="Keyboard", price=Decimal("79.90"), stock=5)
    ]

    response = client.get("/api/v1/products/")

    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "name": "Keyboard", "price": 79.9, "stock": 5}
    ]


@patch("app.modules.product.product_routes.ProductService.create_product")
def test_create_product(mock_create, client):
    mock_create.return_value = Product(
        id=1, name="Keyboard", price=Decimal("79.90"), stock=5
    )

    response = client.post(
        "/api/v1/products/",
        json={"name": "Keyboard", "price": 79.9, "stock": 5},
    )

    assert response.status_code == 201
    assert response.get_json()["id"] == 1
    mock_create.assert_called_once_with({"name": "Keyboard", "price": 79.9, "stock": 5})
