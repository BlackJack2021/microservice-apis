from dotenv import load_dotenv
import os

from typing import Literal

class EnvConfig:
    '''環境変数の設定を責務とするクラス'''
    def __init__(self):
        '''.env ファイルから環境変数に値を注入
        
        環境変数 ENV の値を参照し、適切な .env.xxx から環境変数の注入を実施
        環境変数 ENV には development, production が設定されていることを想定
        もし何も指定されていない場合、production 扱いで実行される
        '''
        env: Literal['development', 'production'] = os.getenv("ENV", 'production')
        dotenv_path = f"../.env.{env}"
        load_dotenv(dotenv_path)
    
    @property
    def kitchen_base_url(self):
        return os.getenv('KITCHEN_BASE_URL')
    
    @property
    def payments_base_url(self):
        return os.getenv('PAYMENTS_BASE_URL')