from typing import List, Optional
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.orders_service import OrdersService
from orders.repository.orders_repository import OrdersRepository
from orders.repository.unit_of_work import UnitOfWork
from orders.types import OrderId
from orders.web.app import app
from orders.web.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema
)

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders(
    cancelled: Optional[bool] = None,
    limit: Optional[int] = None
):
    '''注文情報をリスト化して取得'''
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        results = orders_service.list_orders(
            limit=limit, cancelled=cancelled
        )
    return {'orders': [results.dict() for result in results]}

@app.post(
    '/orders',
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema
)
def create_order(payload: CreateOrderSchema):
    '''注文をデータベースに追加'''
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(repo)
        orders_service = OrdersService(repo)
        items = payload.model_dump()['items']
        for item in items:
            # バリデーションにより、item['size'] は 'small' ではなく Size.small になっている。
            # これを再度文字列の 'small' に戻すには以下の操作が必要。
            item['size'] = item['size'].value
        order = orders_service.place_order(items)
        # dict の中でデータベースセッションの中を参照するものが存在するので、sessionの中で実施
        order_dict = order.dict()
        unit_of_work.commit()
    return order_dict
        
@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: OrderId):
    '''特定の注文情報を取得'''
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = orders_service.get_order(order_id=order_id)
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f'Order with ID {order_id} not found'
        )

@app.put('/order/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: OrderId, order_details: CreateOrderSchema):
    '''指定された注文のデータを更新'''
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            items = order_details.model_dump()['items']
            for item in items:
                item['size'] = item['size'].value
            order = orders_service.update_order(
                order_id=order_id, items=items
            )
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f'Order with ID {order_id} not found.'
        )
            
@app.delete(
    '/order/{order_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_order(order_id: OrderId):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            orders_service.delete_order(order_id=order_id)
            unit_of_work.commit()
        return
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f'Order with ID {order_id} not found'
        )

@app.post('/orders/{order_id}', response_model=GetOrderSchema)
def cancel_order(order_id: OrderId):
    '''注文をキャンセルする処理を実施'''
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = orders_service.cancel_order(order_id=order_id)
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f'Order with ID {order_id} not found.'
        )

@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: OrderId):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = orders_service.pay_order(order_id=order_id)
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f'Order with ID {order_id} not found.'
        )