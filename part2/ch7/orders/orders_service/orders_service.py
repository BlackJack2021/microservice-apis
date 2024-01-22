from repository.interface import OrderRepositoryInterface
from exceptions import OrderNotFoundError

from typing import List
from orders.types import Item, OrderId

class OrdersService:
    def __init__(self, orders_repository: OrderRepositoryInterface):
        self.orders_repository = orders_repository
    
    def place_order(self, items: List[Item]):
        '''データベースレコードを作成して注文を実行'''
        return self.orders_repository.add(items)
    
    def get_order(self, order_id: OrderId):
        '''注文リポジトリにリクエストされたIDを渡して注文の詳細を取得'''
        order = self.orders_repository.get(order_id)
        if order is not None:
            return order
        raise OrderNotFoundError(
            f'Order with id {order_id} not found'
        )
        
    def update_order(self, order_id: OrderId, items: List[Item]):
        '''指定されたIDの注文を更新'''
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f'Order with id {order_id} not found.'
            )
        return self.orders_repository.update(
            order_id,
            {'items': items}
        )
    
    def list_orders(self, **filters):
        '''注文をリスト化して受け取り'''
        limit = filters.pop('limit', None)
        return self.orders_repository.list(limit, **filters)
        
    
    def pay_order(self, order_id: OrderId):
        '''指定されたIDの注文に対する支払い'''
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f'Order with id {order_id} not found'
            )
        order.pay()
        # 注文をスケジュールした後、 schedule_id を更新
        schedule_id = order.schedule()
        return self.orders_repository.update(
            order_id,
            status='progress',
            schedule_id=schedule_id
        )

    def cancel_order(self, order_id: OrderId):
        order = self.orders_repository.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f'Order with id {order_id} not found.'
            )
        order.cancel()
        return self.orders_repository.update(
            order_id,
            status="cancelled"
        )