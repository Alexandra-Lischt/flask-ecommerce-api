from app.extensions import db
from app.modules.product.product_model import Product


def test_product_crud_persists_through_api(client, app):
    payload = {"name": "Keyboard", "price": 79.9, "stock": 5}
    created = client.post("/api/v1/products/", json=payload)
    assert created.status_code == 201
    product_id = created.get_json()["id"]

    fetched = client.get(f"/api/v1/products/{product_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["name"] == "Keyboard"

    updated = client.put(
        f"/api/v1/products/{product_id}",
        json={"name": "Mouse", "price": 39.5, "stock": 8},
    )
    assert updated.status_code == 200
    assert updated.get_json()["name"] == "Mouse"

    deleted = client.delete(f"/api/v1/products/{product_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/products/{product_id}").status_code == 404

    with app.app_context():
        assert db.session.get(Product, product_id) is None
