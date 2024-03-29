# 依存性の注入（Dependency Injection）

## 概要

- 依存性の注入（Dependency Injection, DI）は、ソフトウェア設計の技法で、コンポーネントの依存関係を外部から供給する方法です。これにより、コンポーネントの再利用性、テスト容易性、および保守性が向上します。

## DI の主要なポイント

1. **結合度の低減**: コンポーネントは自身の依存関係を作成するのではなく、外部から提供されます。これにより、コンポーネント間の結合度が低下し、柔軟性が向上します。
2. **テストの容易性**: 依存関係を外部から注入することにより、モックやスタブを使用して依存関係を容易に置き換えることができ、ユニットテストが容易になります。
3. **コードの明瞭さ**: 依存関係が外部から注入されるため、コードの意図がより明確になり、読みやすくなります。

## DI の例

### FastAPI における一般的な例

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 依存関係
def get_db():
    # DBセッションを取得するロジック
    pass

@app.get("/items/")
def read_items(db = Depends(get_db)):
    # ここでDBセッションを使用
    pass
```

- この例では、`Depends(get_db)` を使用して `get_db` 関数からデータベースセッションを依存性として注入しています。FastAPI がリクエストごとに適切なタイミングで `get_db` を呼び出し、DB セッションを `read_items` 関数に提供します。

### `orders_service.py` における例

以下の実装は良くない例。何故なら、注文リポジトリのインポートとインスタンス化を注文サービスが引き受けてしまっており、責任が重たい。

```py
from repository.orders_repository import OrdersRepository
class OrdersService:
    def __init__(self):
        self.repository = OrdersRepository()
```

こうではなく、注文リポジトリのインスタンス化と設定を正しく行う責任を呼び出し元にゆだねられる
以下のアプローチの方が、適切な依存性の注入を行えている。

```py
from repository.interface import OrderRepositoryInterface
class OrdersService:
    def __init__(self, orders_repository: OrderRepositoryInterface):
        self.orders_repository = orders_repository
```

## まとめ

依存性の注入は、アプリケーションのコンポーネントをより疎結合にし、コードの再利用性、テスト容易性、および保守性を向上させる効果的な手法です。特に、フレームワークやライブラリを利用するモダンなソフトウェア開発において、この技法は広く採用されています。

# 制御の反転（Inversion of Control）とは

## 概要

- 制御の反転（Inversion of Control, IoC）は、ソフトウェアエンジニアリングにおける設計原則の一つであり、プログラムの実行フローの制御をアプリケーションのカスタムコードから切り離し、フレームワークやライブラリに委ねるアプローチです。

## IoC の主要なポイント

1. **制御フローの委譲**: アプリケーションのコードは「何をするか」を定義し、フレームワークやライブラリが「いつ、どのように」実行するかを決定します。
2. **コードの再利用性とテスト容易性の向上**: フレームワークが制御を担うことで、コードの再利用性が向上し、テストが容易になります。
3. **柔軟性と拡張性の向上**: フレームワークに制御を任せることで、アプリケーションは柔軟かつ拡張しやすい構造になります。

## FastAPI における IoC の例

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

- **いつ**: `@app.get("/")` デコレータは FastAPI に「HTTP GET リクエストが "/" に対して来た場合にこの関数を実行する」と伝えます。リクエストの受付、解析、ルーティングは FastAPI が担当します。
- **どのように**: `read_root` 関数は JSON レスポンスを返しますが、HTTP レスポンスの構築は FastAPI が行います。開発者はレスポンスの内容を定義するだけです。

## まとめ

制御の反転は、アプリケーションのロジックから低レベルの実行の詳細を分離し、開発者がビジネスロジックに集中できるようにする設計原則です。フレームワークやライブラリの効果的な利用により、コードはよりモジュラーでテストしやすく、拡張しやすいものになります。
