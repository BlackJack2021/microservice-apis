import requests

from typing import Optional

from orders.orders_service.exceptions import (
    APIIntegrationError,
    InvalidActionError
)
from orders.repository.models import OrderModel

class OrderItem:
    def __init__(self, id, product, quantity, size):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.size = size

    def dict(self):
        return {
            'product': self.product,
            'size': self.size,
            'quantity': self.quantity
        }

class Order:
    def __init__(
        self,
        id,
        created,
        items,
        status,
        schedule_id=None,
        delivery_id=None,
        order_: Optional[OrderModel]=None
    ):
        '''ビジネスロジックで用いるための Order オブジェクトの定義
        
        Args:
            order_ (Optional[OrderModel]): データベースオブジェクトへの参照。
                                           データベーストランザクションをコミットした後に注文のIDにアクセスするのに役立つ。
        '''
        self._order = order_
        self._id = id
        self._created = created
        self.items = [OrderItem(**item) for item in items]
        self._status = status
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id
        
    @property
    def id(self):

        return self._id or self._order.id
    
    @property
    def created(self):
        return self._created or self._order.created
    
    @property
    def status(self):
        return self._status or self._order.status