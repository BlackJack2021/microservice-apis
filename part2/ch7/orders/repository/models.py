import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# 宣言的なベースモデルを作成
Base = declarative_base()

# モデルのランダムなUUIDを作成するカスタム関数
def generate_uuid():
    return str(uuid.uuid4())

class OrderModel(Base):
    # このモデルにマッピングするテーブルの名前
    __tablename__ = 'order'
    
    # 各クラスプロパティは Column クラスを使ってデータベースの列にマッピングされる
    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )
    # relationship() を使って OrderItemModel と1対多の関係を確立
    items = relationship('OrderItemModel', backref='order')
    status = Column(String, nullable=False, default='created')
    created = Column(DateTime, default=datetime.utcnow)
    schedule_id = Column(String)
    delivery_id = Column(String)
    
    # オブジェクトを Python ディクショナリとしてレンダリングするカスタムメソッド
    def dict(self):
        return {
            'id': self.id,
            'items': [item.dict() for item in self.items],
            'status': self.status,
            'created': self.created,
            'schedule_id': self.schedule_id,
            'delivery_id': self.delivery_id
        }

class OrderItemModel(Base):
    __tablename__ = 'order_item'
    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )
    order_id = Column(
        Integer,
        ForeignKey('order.id')
    )
    product = Column(String, nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    
    def dict(self):
        return {
            'id': self.id,
            'product': self.product,
            'size': self.size,
            'quantity': self.quantity
        }