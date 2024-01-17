from sqlalchemy.orm import Session

from typing import Optional

from orders.domain.order import Order
from orders.repository.models import OrderModel, OrderItemModel
from orders.repository.interface import OrderRepositoryInterface

class OrdersRepository(OrderRepositoryInterface):
    
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, items):
        '''データベースに、複数のアイテムを保存する'''
        # 注文のレコードを作成する際、注文内のアイテムごとにレコードを作成
        record = OrderModel(
            items=[OrderItemModel(**item) for item in items]
        )
        # セッションオブジェクトにレコードを追加
        self.session.add(record)
        # Order クラスのインスタンスを返す
        return Order(**record.dict(), order_=record)
    
    def _get(self, id_) -> OrderModel | None:
        '''特定の注文データを取得
        
        SQLAlchemy の first メソッドを利用し、データオブジェクトとして出力
        '''
        return (
            self.session
                .query(OrderModel)
                .filter(OrderModel.id == str(id_))
                .first()
        )
        
    def get(self, id_) -> Order | None:
        '''特定の注文データを Order オブジェクトの形で出力
        
        Order はビジネスロジックで用いるオブジェクト
        '''
        order = self._get(id_)
        if order is not None:
            return Order(**order.dict())
        
    def list(
        self,
        limit: Optional[int],
        **filters
    ):
        query = self.session.query(OrderModel)
        # SQLAlchemy の filter メソッドを使って、
        # 注文がキャンセルされているかどうかでフィルタリング
        if 'cancelled' in filters:
            cancelled = filters.pop('cancelled')
            if cancelled:
                query = query.filter(OrderModel.status == 'cancelled')
            else:
                query = query.filter(OrderModel.status != 'cancelled')
        
        # 他にも filter が指定されている場合、その filter の条件に基づいてフィルタリング
        # さらに、limit の数を上限とするようにデータ数を絞り込み
        records = query.filter_by(**filters).limit(limit).all()
        
        # ビジネスロジックに利用する Order オブジェクト のリストを返却
        return [Order(**record.dict()) for record in records]
    
    def update(self, id_, **payload):
        '''与えられた payload の情報を元に注文データを更新'''
        record = self._get(id_)

        # 商品データについて
        if 'item' in payload:
            # まずは record のアイテムを全て削除
            for item in record.items:
                self.session.delete(item)
            # 続いて、payload からアイテムを追加
            record.items = [
                OrderItemModel(**item) for item in payload.pop('items')
            ]
        
        # その他のデータを更新
        for key, value in payload.items():
            # setattr という組込み関数を利用することでシンプルにプロパティの値を変更できる
            # ただし、key が record に存在しない場合は勝手に追加されてしまう点に注意
            setattr(record, key, value)
        return Order(**record.dict())
            
    def delete(self, id_):
        '''指定された注文データを削除'''
        self.session.delete(self._get(id_))
        