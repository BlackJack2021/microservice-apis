'''注文サービスのビジネスロジックで利用される注文オブジェクトを定義

現時点ではまだ仮実装
'''

import requests
from orders.orders_service.exceptions import (
    APIIntegrationError,
    InvalidActionError
)
from orders.types import ScheduleId

from config.env_config import EnvConfig

class OrderItem:
    '''注文の各アイテムを表すビジネスオブジェクト'''
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
        order_=None
    ):
        '''イニシャライザ
        
        **id, created, status についての補足**
        注文の作成時刻やIDといった注文の一部のプロパティはデータ層によって設定されるため、
        データベースへの変更がコミットされた後でなければ知ることはできない。
        変更内容のコミットはリポジトリのスコープ外であるため、
        注文リポジトリに追加したときに返されるオブジェクトには、それらのプロパティが含まれていないことになる。
        注文のIDとその作成時刻が利用できる状態になるのはトランザクションをコミットした後であり、
        注文のデータベースレコードを通じて提供される。
        このため、イニシャライザでは注文のID、作成時刻、ステータスを先頭にアンダースコアが付いた
        プライベートプロパティとしてバインドする。
        その上で、Order クラスの order_パラメータを使って、注文のデータベースレコードに対するポインタを保持する。
        既にデータベースに保存されている注文の詳細を取得する場合、_id, _created, _status には対応する値が割り当てられる。
        しかし、それ以外の場合では None が当てられており、その場合はポインタから取得することになる。
        この実装を property デコレータを通じて行っている。
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
    
    def cancel(self):
        '''注文のキャンセルを実施
        
        status が progress ならキャンセルを実施、
        delivery であればキャンセルせず、エラーを出力
        '''
        kitchen_base_url = EnvConfig().kitchen_base_url
        if self.status == 'progress':
            response = requests.post(
                f"{kitchen_base_url}/schedules/{self.schedule_id}/cancel",
                json={"order": [item.dict() for item in self.items]}
            )
            
            if response.status_code == 200:
                return
            
            raise APIIntegrationError(
                f'Could not cancel order with id {self.id}'
            )
        
        # 配達中の注文のキャンセルは許可しない
        if self.status == 'delivery':
            raise InvalidActionError(
                f'Could not process payment for order with id {self.id}'
            )
        
    def pay(self):
        '''支払いサービスを利用して支払いを実行'''
        payments_base_url = EnvConfig().payments_base_url
        response = requests.post(
            payments_base_url,
            json={'order_id': self.id}
        )
        if response.status_code == 201:
            return
        raise APIIntegrationError(
            f'Could not process payment for order with id {self.id}'
        )
        
    def schedule(self) -> ScheduleId:
        '''厨房サービスに注文内容をスケジューリング'''
        kitchen_base_url = EnvConfig().kitchen_base_url
        items = [item.dict() for item in self.items]
        response = requests.post(
            f'{kitchen_base_url}/schedules',
            json = {'order': items}
        )
        # 厨房サービスから成功のレスポンスを受け取った場合は、schedule_id を返却
        if response.status_code == 201:
            return response.json()['id']
        raise APIIntegrationError(
            f'Could not schedule order with id {self.id}'
        )
    