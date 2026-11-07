from apiflask.fields import Decimal, Integer, String
from apiflask.schemas import Schema
from marshmallow.validate import Range


class ProductCreateSchema(Schema):
    name = String(required=True)
    price = Decimal(required=True)
    stock = Integer(required=True, validate=Range(min=0))
    category = String(required=True, metadata={"description": "Categoria do produto"})
    description = String(
        required=True, metadata={"description": "Descrição do produto"}
    )


class ProductResponseSchema(Schema):
    id = Integer(dump_only=True)
    name = String()
    price = Decimal(as_string=True)
    stock = Integer()
    category = String()
    description = String()
    created_at = String()
