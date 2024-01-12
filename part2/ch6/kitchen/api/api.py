import copy
import uuid
from datetime import datetime
from typing import Dict, Any, List

from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError
from flask import abort

# marshmallow モデルをインポート
from .schemas import (
    GetScheduledOrderSchema,
    ScheduleOrderSchema,
    GetScheduledOrdersSchema,
    ScheduleStatusSchema,
    GetKitchenScheduleParameters
)

# 型ヒントをインポート
from .type import (
    EachOrder,
    Schedule,
    ScheduleOrder
)

blueprint = Blueprint('kitchen', __name__, description='Kitchen API')

# インメモリでスケジュールを定義
schedules: List[Schedule] = []

# データ検証コードを関数として切り出し
def validate_schedule(schedule: Schedule):
    # schedule に変更を加えても、直ちに破壊的変更にならないことを保証
    _schedule = copy.deepcopy(schedule)
    _schedule['scheduled'] = schedule['scheduled'].isoformat()
    errors = GetScheduledOrderSchema().validate(_schedule)
    if errors:
        ValidationError(errors)
    

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
            validate_schedule(schedule)
        
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
    def post(self, payload: ScheduleOrder):
        '''IDなどのサーバー側のスケジュールの属性を設定'''
        
        payload['id'] = str(uuid.uuid4())
        payload['scheduled'] = datetime.utcnow()
        payload['status'] = 'pending'
        validate_schedule(payload)
        schedules.append(payload)
        return payload
    
# URL パラメータは <> で囲んで定義
@blueprint.route('/kitchen/schedules/<schedule_id>')
class KitchenSchedule(MethodView):
    
    @blueprint.response(
        status_code=200,
        schema=GetScheduledOrderSchema
    )
    def get(self, schedule_id: str):
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                validate_schedule(schedule)
                return schedule
        abort(
            404,
            description=f'Resource with ID {schedule_id} not found'
        )
    
    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(
        status_code=200,
        schema=GetScheduledOrderSchema
    )
    def put(self, payload: ScheduleOrder, schedule_id: str):
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                schedule.update(payload)
                validate_schedule(schedule)
                return schedule
        abort(
            404,
            description=f"Resource with ID {schedule_id} not found"
        )

    @blueprint.response(status_code=204)
    def delete(self, schedule_id: str):
        for index, schedule in enumerate(schedules):
            if schedule['id'] == schedule_id:
                schedules.pop(index)
                return
        abort(
            404,
            description=f'Resource with ID {schedule_id} not found'
        )
    
# URL パス　/kitchen/schedules/<schedule_id>/cancel を関数ベースのビューとして実装
@blueprint.response(
    status_code=200,
    schema=GetScheduledOrderSchema
)
@blueprint.route('/kitchen/schedules/<schedule_id>/cancel', methods=['POST'])
def cancel_schedule(schedule_id: str):
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            schedule['status'] = 'cancelled'
            validate_schedule(schedule)
            return schedule
    abort(
        404,
        description=f'Resource with ID {schedule_id} not found'
    )

@blueprint.response(
    status_code=200,
    schema=ScheduleStatusSchema
)
@blueprint.route('/kitchen/schedules/<schedule_id>/status', methods=['GET'])
def get_schedule_status(schedule_id: str):
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            validate_schedule(schedule)
            return {'status': schedule['status']}
    abort(
        404,
        description=f'Resource with ID {schedule_id} not found.'
    )