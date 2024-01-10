import uuid
from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint

blueprint = Blueprint('kitchen', __name__, description='Kitchen API')

# ハードコーディングされたスケジュールのリストを宣言
schedules = [
    {
        'id': str(uuid.uuid4()),
        'scheduled': datetime.now(),
        'status': 'pending',
        'order': [
            {
                'product': 'cappuccino',
                'quantity': 1,
                'size': 'big'
            }
        ]
    }
]

# Blueprint の route() デコレータを使って、クラスまたは関数をURLパスとして登録
@blueprint.route('/kitchen/schedules')
# URL パス /kitchen/schedules をクラスベースのビューとして実装
# ビュー : Webアプリケーションにおける特定のURLリクエストを処理するロジック
class KitchenSchedules(MethodView):
    def get(self):
        return {
            'schedules': schedules
        }, 200
    
    def post(self, payload):
        return schedules[0], 201
    
# URL パラメータは <> で囲んで定義
@blueprint.route('/kitchen/schedules/<schedule_id>')
class KitchenSchedule(MethodView):
    def get(self, schedule_id):
        return schedules[0], 200
    
    def post(self, payload, schedule_id):
        return schedules[0], 200

    def delete(self, schedule_id):
        return '', 204
    
# URL パス　/kitchen/schedules/<schedule_id>/cancel を関数ベースのビューとして実装
@blueprint.route('/kitchen/schedules/<schedule_id>/cancel', methods=['POST'])
def cancel_schedule(schedule_id):
    return schedules[0], 200

@blueprint.route('/kitchen/schedules/<schedule_id>/status', methods=['GET'])
def get_schedule_status(schedule_id):
    return schedules[0], 200