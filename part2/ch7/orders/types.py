from typing import TypedDict, Optional, List
from uuid import UUID
from datetime import datetime

# ID の型
ItemId = UUID
OrderId = UUID
ScheduleId = UUID

# 商品の型
class Item(TypedDict):
    id: Optional[ItemId]
    product: str
    size: str
    quantity: str

# 注文データの型
class OrderRecord(TypedDict):
    id: OrderId
    items: List[Item]
    status: str
    created: datetime
    schedule_id: str
    delivery_id: str