from decimal import Decimal
from unittest.mock import patch

import pytest
from apiflask import HTTPError

from app.modules.product.product_service import ProductService


@patch("app.modules.product.product_service.db.session")
def test_create_product_commits(mock_session, memory_product_repo):
    service = ProductService(memory_product_repo)

    product = service.create_product({"name": "Keyboard", "price": 79.9, "stock": 5})

    assert product.name == "Keyboard"
    assert product.price == Decimal("79.9")
    assert memory_product_repo.get_by_id(product.id) is product
    mock_session.commit.assert_called_once()


@patch("app.modules.product.product_service.db.session")
def test_create_product_rolls_back_on_failure(mock_session, memory_product_repo):
    memory_product_repo.save = lambda product: (_ for _ in ()).throw(RuntimeError())
    service = ProductService(memory_product_repo)

    with pytest.raises(HTTPError) as error:
        service.create_product({"name": "Keyboard", "price": 10, "stock": 1})

    assert error.value.status_code == 500
    mock_session.rollback.assert_called_once()


def test_get_product_returns_404_when_missing(memory_product_repo):
    with pytest.raises(HTTPError) as error:
        ProductService(memory_product_repo).get_product(99)

    assert error.value.status_code == 404
