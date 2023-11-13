from fastapi import APIRouter

from utils.exceptions import try_except_decorator
from utils.dependency import OrdersServiceDep

from .schemas import Order

router = APIRouter(prefix='/orders', tags=['Orders'])


@router.post('')
@try_except_decorator
async def post_order_handler(order: Order,
                             orders_service: OrdersServiceDep):
    await orders_service.add_order(order)
    return {
        'data': None,
        'details': 'Order was added.'
    }
