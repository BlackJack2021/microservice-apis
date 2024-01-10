from fastapi import FastAPI
from pathlib import Path
import yaml

# FastAPIクラスのインスタンスを作成。このオブジェクトはAPIアプリケーションを表す
app = FastAPI(
    debug=True,
    openapi_url='/openapi/orders.json',
    docs_url='/docs'
)

# PyYAML を使って API 仕様書をロード
print(Path(__file__).parent)
oas_doc = yaml.safe_load(
    (Path(__file__).parent / 'oas.yaml').read_text()
)

# FastAPI の openapi プロパティを上書きし、API仕様書を返すようにする
app.openapi = lambda: oas_doc

# api モジュールをインポートし、読み込み時にビュー関数を登録できるようにする
from api import api