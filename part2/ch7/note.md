# ヘキサゴナルアーキテクチャとデータベースの抽象化

ヘキサゴナルアーキテクチャの目的の一つは、アプリケーションのビジネスロジックを、その他の部分（例えばデータベースや UI）から疎結合に保つことです。これにより、それぞれの部分が独立して変更やテストが可能になります。

具体的には、データベースへのアクセスを抽象化するレイヤー（リポジトリパターンなど）を導入することで、ビジネスロジックはデータがどのように保存されているか、どのデータベース技術が使用されているかを知らなくても良い状態を作り出します。これにより、データベースの具体的な実装を変更する場合でも、その影響がビジネスロジックに及ばないようにすることが可能になります。

## ヘキサゴナルアーキテクチャの具体例

以下に、FastAPI を用いてヘキサゴナルアーキテクチャで Todo リストの機能を実装する基本的な例を示します。

```py
# logic.py
class TodoService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_todos(self):
        return self.repository.get_all()

    def add_todo(self, title):
        self.repository.add(title)

# cruds.py
class TodoRepository:
    def __init__(self):
        self.todos = []

    def get_all(self):
        return self.todos

    def add(self, title):
        self.todos.append(title)

# router.py
from fastapi import FastAPI
app = FastAPI()

repository = TodoRepository()
service = TodoService(repository)

@app.get("/todos")
def get_all_todos():
    return service.get_all_todos()

@app.post("/todos")
def add_todo(title: str):
    service.add_todo(title)
    return {"message": "Todo added successfully"}
```

この例では、`TodoService`クラスがアプリケーションのコアロジックを表し、`TodoRepository`クラスがデータベースへのアクセスを抽象化しています。FastAPI のルート関数は、HTTP リクエストを処理するアダプタとして機能します。これにより、アプリケーションのコアロジックは、HTTP リクエストの詳細やデータベースの具体的な実装から疎結合に保たれます。

## ポートとリポジトリ

ヘキサゴナルアーキテクチャにおける"ポート"は、アプリケーションのコアビジネスロジックと外部の世界（データベース、UI、外部システムなど）との間に明確な境界を設けます。これにより、コアロジックは外部の変更から隔離され、各部分が独立して変更やテストが可能になります。

リポジトリは、データの取得や保存といった操作を提供しますが、それがどのように実現されるか（例えば SQL クエリや NoSQL クエリ）は定義しません。これにより、ビジネスロジックはデータがどのように保存されているか、どのデータベース技術が使用されているかを知らなくて
