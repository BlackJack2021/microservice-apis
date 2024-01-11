import copy
import uuid
from datetime import datetime
from typing import Dict, Any

from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

# marshmallow モデルをインポート
from .schemas import (
    GetScheduledOrderSchema,
    ScheduleOrderSchema,
    GetScheduledOrdersSchema,
    ScheduleStatusSchema,
    GetKitchenScheduleParameters
)

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
    
    @blueprint.arguments(
        GetKitchenScheduleParameters,
        location='query'
    )
    # Bluepring の response() デコレータを使って、
    # レスポンスペイロードの marshmallow モデルを登録
    @blueprint.response(
        status_code=200,
        schema=GetScheduledOrdersSchema
    )    
    def get(self, parameters: Dict[str, Any]):
        
        # まず初めに、データベースから取得されることが想定される schedules について
        # 正しいデータが含まれることを検証する
        for schedule in schedules:
            schedule = copy.deepcopy(schedule)
            schedule['scheduled'] = schedule['scheduled'].isoformat()
            errors = GetScheduledOrderSchema().validate(schedule)
            if errors:
                raise ValidationError(errors)
        
        # パラメータが特に指定されていない場合はスケジュールのリストを返す
        if not parameters:
            return {'schedules': schedules}
        # ユーザーがURLクエリパラメータを設定した場合は、
        # それらを使ってスケジュールのリストをフィルタリング
        query_set = [schedule for schedule in schedules]
        
        # progress パラメータの処理
        in_progress = parameters.get('progress')
        if in_progress is not None:
            if in_progress:
                query_set = [
                    schedule for schedule in schedules
                    if schedule['status'] == 'progress'
                ]
            else:
                query_set = [
                    schedule for schedule in schedules
                    if schedule['status'] != 'progress'    
                ]
        
        # since パラメータの処理
        since = parameters.get('since')
        if since is not None:
            query_set = [
                schedule for schedule in schedules
                if schedule['scheduled'] >= since
            ]
        
        # limit の処理
        limit = parameters.get('limit')
        if limit is not None and len(query_set) > limit:
            query_set = query_set[:limit]
        
        return {'schedules': query_set}
            
    # Blueprint の arguments() デコレータを使って、
    # レスポンスペイロードの marshmallow モデルを登録
    @blueprint.arguments(ScheduleOrderSchema)
    # status_code パラメータの値を目的のステータスコードに設定
    @blueprint.response(
        status_code=201,
        schema=GetScheduledOrderSchema
    )
    def post(self, payload):
        return schedules[0]
    
# URL パラメータは <> で囲んで定義
@blueprint.route('/kitchen/schedules/<schedule_id>')
class KitchenSchedule(MethodView):
    
    @blueprint.response(
        status_code=200,
        schema=GetScheduledOrderSchema
    )
    def get(self, schedule_id):
        return schedules[0]
    
    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(
        status_code=200,
        schema=GetScheduledOrderSchema
    )
    def post(self, payload, schedule_id):
        return schedules[0], 200

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        return
    
# URL パス　/kitchen/schedules/<schedule_id>/cancel を関数ベースのビューとして実装
@blueprint.response(
    status_code=200,
    schema=GetScheduledOrderSchema
)
@blueprint.route('/kitchen/schedules/<schedule_id>/cancel', methods=['POST'])
def cancel_schedule(schedule_id):
    return schedules[0]

@blueprint.response(
    status_code=200,
    schema=ScheduleStatusSchema
)
@blueprint.route('/kitchen/schedules/<schedule_id>/status', methods=['GET'])
def get_schedule_status(schedule_id):
    return schedules[0]