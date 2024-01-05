from fastapi import FastAPI

# FastAPIクラスのインスタンスを作成。このオブジェクトはAPIアプリケーションを表す
app = FastAPI(debug=True)

# api モジュールをインポートし、読み込み時にビュー関数を登録できるようにする
from orders.api import api