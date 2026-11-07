from decimal import Decimal

from app.extensions import db
from app.modules.product.product_model import Product
from app.modules.product.product_repo import ProductRepository


def test_repository_crud(app):
    with app.app_context():
        repo = ProductRepository()
        product = Product(name="Keyboard", price=Decimal("79.90"), stock=5)

        repo.save(product)
        db.session.commit()

        assert repo.list_all() == [product]
        assert repo.get_by_id(product.id) == product

        product.stock = 8
        repo.save(product)
        db.session.commit()
        assert repo.get_by_id(product.id).stock == 8

        repo.delete(product)
        db.session.commit()
        assert repo.get_by_id(product.id) is None
