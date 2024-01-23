from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, conint, conlist, validator


class Size(Enum):
    small = 'small'
    medium = 'medium'
    big = 'big'


class Status(Enum):
    created = 'created'
    paid = 'paid'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    # quantityフィールドはOptionalとして定義されていますが、
    # これはフィールドが存在しない場合を許容するためです。
    # しかし、フィールドが存在するがNoneである場合は許容されません。
    # この微妙な違いを表現するために、quantity_non_nullableバリデーターが使用されています。
    quantity: Optional[conint(ge=1, strict=True)] = 1

    class Config:
        extra = 'forbid'

    @validator('quantity')
    # このバリデーターは、quantityフィールドがNoneでないことを確認します。
    # もしNoneであれば、'quantity may not be None'というメッセージと共にAssertionErrorが発生します。
    def quantity_non_nullable(cls, value):
        assert value is not None, 'quantity may not be None'
        return value


class CreateOrderSchema(BaseModel):
    items: conlist(OrderItemSchema, min_items=1)

    class Config:
        extra = 'forbid'


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: Status


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]

    class Config:
        extra = 'forbid'