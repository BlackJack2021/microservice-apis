from flask import Flask
from flask_smorest import Api
from .config import BaseConfig
from .api.api import blueprint

from pathlib import Path
import yaml
from apispec import APISpec

# Flask アプリケーションオブジェクトのインスタンスを作成
app = Flask(__name__)

# from_object メソッドを使って、クラスから設定を読み込む
app.config.from_object(BaseConfig)

# flask-smorest のApi オブジェクトのインスタンスを作成
kitchen_api = Api(app)

# Blueprint を厨房APIオブジェクトに登録
kitchen_api.register_blueprint(blueprint)

oas_file = (Path(__file__).parent / "oas.yaml").read_text()
api_spec = yaml.safe_load(oas_file)
spec = APISpec(
    title=api_spec['info']['title'],
    version=api_spec['info']['version'],
    openapi_version=api_spec['openapi']
)
spec.to_dict = lambda: api_spec
kitchen_api.spec = spec