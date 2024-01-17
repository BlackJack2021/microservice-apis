# 以下の実装は良くない例。何故なら、注文リポジトリのインポートとインスタンス化を注文サービスが引き受けてしまっており、責任が重たい。
#from repository.orders_repository import OrdersRepository
#class OrdersService:
#    def __init__(self):
#        self.repository = OrdersRepository()

# 以下の「依存性の注入」を利用したパターンでは、
# 注文リポジトリのインスタンス化と設定を正しく行う責任を呼び出し元にゆだねられる。
from repository.interface import OrderRepositoryInterface
class OrdersService:
    def __init__(self, orders_repository: OrderRepositoryInterface):
        self.orders_repository = orders_repository