from flask import Flask
from flask_smorest import Api
from .config import BaseConfig
from .api.api import blueprint

# Flask アプリケーションオブジェクトのインスタンスを作成
app = Flask(__name__)

# from_object メソッドを使って、クラスから設定を読み込む
app.config.from_object(BaseConfig)

# flask-smorest のApi オブジェクトのインスタンスを作成
kitchen_api = Api(app)

# Blueprint を厨房APIオブジェクトに登録
kitchen_api.register_blueprint(blueprint)

