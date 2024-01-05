import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status
from http import HTTPStatus

from app import app
from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema
)

# インメモリの注文リストを Python のリストとして表現
ORDERS = []

orders = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': 'delivered',
    'created': datetime.utcnow(),
    'order': [
        {
            'product': 'cappuccino',
            'size': 'medium',
            'quantity': 1
        }
    ]
}

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    return {
        'orders': ORDERS
    }

@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(
    order_details: CreateOrderSchema,
    response_model=GetOrderSchema
):
    order = order_details.model_dump()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    # 注文を作成するには、その注文をリストに追加
    ORDERS.append(order)
    return order

@app.get('/orders/{order_id}')
def get_order(order_id: UUID):
    # 注文をIDで検索
    for order in ORDERS:
        if order['id'] == order_id:
            return order
    # 注文が見つからない場合は status_code を 404 に設定したうえで、
    # HTTPException を生成
    raise HTTPException(
        status_code=404,
        detail=f'Order with ID {order_id} not found'
    )

@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.model_dump())
            return order
    raise HTTPException(
        status_code=404,
        detail=f"Order with ID {order_id} not found."
    )

@app.delete(
    '/orders/{order_id}', 
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise HTTPException(
        status_code=404,
        detail=f'Order with ID {order_id} not found'
    )
    
@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cance(lled'
            return order
    raise HTTPException(
        status_code=404,
        detail=f'Order with ID {order_id} not found'
    )

@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException(
        status_code=404,
        detail=f'Order with ID {order_id} not found'
    )