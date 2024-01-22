from abc import ABC, abstractmethod
from typing import List, Optional

from orders.domain.order import Order
from sqlalchemy.orm import Session
from orders.types import Item, OrderId

class OrderRepositoryInterface(ABC):
    """OrderRepositoryクラスのインターフェイス

    このインターフェイスは、OrderRepository クラスやそれに類似したクラスの設計の基礎です。
    実際のデータベース操作に関するメソッドを定義します。

    Attributes:
        session (Session): SQLAlchemy の Session インスタンス。
    """

    @abstractmethod
    def __init__(self, session: Session):
        """コンストラクタ

        Args:
            session (Session): SQLAlchemy のセッション。
        """
        pass

    @abstractmethod
    def add(self, items: List[Item]) -> Order:
        """注文アイテムをデータベースに追加し、Order オブジェクトを返します。

        Args:
            items (List[Item]): 注文アイテムのリスト。

        Returns:
            Order: 追加された注文データ。
        """
        pass

    @abstractmethod
    def get(self, id_: OrderId) -> Optional[Order]:
        """指定されたIDの注文データを取得します。

        Args:
            id_ (OrderId): 注文のID。

        Returns:
            Optional[Order]: 注文データの Order オブジェクト。存在しない場合は None。
        """
        pass

    @abstractmethod
    def list(self, limit: Optional[int], **filters) -> List[Order]:
        """指定された条件で注文データのリストを取得します。

        Args:
            limit (int, optional): 取得する注文の最大数。
            **filters: 注文データをフィルタリングするための追加キーワード引数。

        Returns:
            List[Order]: 条件に一致する注文データのリスト。
        """
        pass

    @abstractmethod
    def update(self, id_: OrderId, **payload) -> Order:
        """指定されたIDの注文データを更新します。

        Args:
            id_ (OrderId): 更新する注文のID。
            **payload: 更新するデータのキーワード引数。

        Returns:
            Order: 更新された注文データ。
        """
        pass

    @abstractmethod
    def delete(self, id_: OrderId):
        """指定されたIDの注文データを削除します。

        Args:
            id_ (OrderId): 削除する注文のID。
        """
        pass
