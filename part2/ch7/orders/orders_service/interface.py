
from abc import ABC, abstractmethod
from repository.interface import OrderRepositoryInterface

class OrdersServiceInterface(ABC):
    '''注文サービスクラスが持つべき特徴を示したインターフェイスです
    
    OrderService クラス、及びテストなどの目的で構築されるそれに準ずるクラスを実装する場合に
    こちらのインターフェイスを継承して構築してください。
    '''
    @abstractmethod
    def __init__(self, orders_repository: OrderRepositoryInterface):
        self.orders_repository = orders_repository
    
    @abstractmethod    
    def place_order(self, items):
        '''注文を作成'''
        pass

    @abstractmethod
    def get_order(self, order_id):
        '''指定された order_id の注文の詳細を取得'''
        pass

    @abstractmethod
    def update_order(self, order_id, items):
        '''指定された order_id の注文データを更新'''
        pass

    @abstractmethod
    def list_orders(self, **filters):
        '''注文をリストアップして出力'''
        pass

    @abstractmethod
    def pay_order(self, order_id):
        '''指定された order_id の注文の支払いを実行'''
        pass

    @abstractmethod
    def cancel_order(self, order_id):
        pass
    