from apiflask.fields import (
    UUID,
    DateTime,
    Decimal,
    Integer,
    List,
    Nested,
    String,
)
from apiflask.schemas import Schema
from marshmallow.validate import Length, Range


class OrderItemCreateSchema(Schema):
    product_id = UUID(required=True)
    quantity = Integer(required=True, strict=True, validate=Range(min=1))


class OrderCreateSchema(Schema):
    user_id = UUID(required=True)
    items = List(Nested(OrderItemCreateSchema), required=True, validate=Length(min=1))


class OrderItemResponseSchema(Schema):
    id = UUID(dump_only=True)
    product_id = UUID(dump_only=True)
    quantity = Integer()
    price_at_purchase = Decimal(as_string=True)


class OrderResponseSchema(Schema):
    id = UUID(dump_only=True)
    user_id = UUID(dump_only=True)
    status = String()
    total_price = Decimal(as_string=True)
    items = List(Nested(OrderItemResponseSchema))
    created_at = DateTime()
    updated_at = DateTime()
