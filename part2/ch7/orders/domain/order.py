'''注文サービスのビジネスロジックで利用される注文オブジェクトを定義

現時点ではまだ仮実装
'''

class OrderItem:
    '''注文の各アイテムを表すビジネスオブジェクト'''
    def __init__(self, id, product, quantity, size):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.size = size
        
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