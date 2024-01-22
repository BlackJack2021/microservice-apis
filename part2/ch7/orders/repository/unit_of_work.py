'''UnitOfWork クラスの定義モジュール。

SQLAlchemy の詳細を理解せずとも、ビジネスロジックが

- セッションの開閉
- コミット
- ロールバック

を実施することのできるコンテキストマネージャーを定義することが目的。
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Optional, Type, TracebackType

class UnitOfWork:
    
    def __init__(self):
        # 一旦ローカルの sqlite を参照するようにハードコーディング
        self.session_maker = sessionmaker(
            bind=create_engine('sqlite:///orders.db')
        )
    
    def __enter__(self):
        '''コンテキストマネージャー開始時の処理
        
        この段階で初めて、データベースとの接続を開始する
        '''
        self.session = self.session_maker()
        # UnitOfWork オブジェクトのインスタンスを返す
        return self
    
    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        traceback: Optional[TracebackType]
    ) -> None:
        """
        コンテキストマネージャが終了するときに呼び出されるメソッド。

        Args:
            exc_type (Optional[Type[BaseException]]): ブロック内で発生した例外の型。例外が発生しなかった場合はNone。
            exc_val (Optional[BaseException]): ブロック内で発生した例外インスタンス。例外が発生しなかった場合はNone。
            traceback (Optional[TracebackType]): ブロック内で発生した例外のトレースバック。例外が発生しなかった場合はNone。
        """
        # 例外が発生した場合はトランザクションをロールバックし、データベース接続を閉じる
        if exc_type is not None:
            self.rollback()
            self.session.close()

        # 例外が発生していない場合でも、
        # コンテキストマネージャーの処理が終了したらデータベース接続を閉じる
        self.session.close()
        
    def commit(self):
        '''データベースのコミットを行う
        
        SQLAlchemy を使い続ける限りは、これは無駄なコードに思えるかもしれないが、
        もし別のフレームワークを使いたくなった時のために、ラッパーを作成。
        '''
        self.session.commit()
        
    def rollback(self):
        self.session.rollback()
    
    