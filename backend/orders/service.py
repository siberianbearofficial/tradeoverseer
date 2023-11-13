from requests import get
from datetime import datetime
from pytz import timezone

from utils.config import ORDERS_NOTIFICATION_CHATS, ORDERS_NOTIFICATION_BOT_TOKEN

from .schemas import Order


class OrdersService:
    def __init__(self):
        pass

    async def add_order(self, order: Order):
        now = datetime.now(tz=timezone("Europe/Moscow")).strftime("%d/%m/%Y, %H:%M:%S")
        msg = (f'Новое обращение ({now})\n'
               f'Подписка: {order.selected}\n'
               f'Способ связи: {order.method}\n'
               f'Контакт: {order.contact}')
        for chat_id in ORDERS_NOTIFICATION_CHATS:
            get(self.prepare_url(msg, chat_id))

    @staticmethod
    def prepare_url(msg, chat_id):
        return (f'https://api.telegram.org/bot'
                f'{ORDERS_NOTIFICATION_BOT_TOKEN}'
                f'/sendMessage?chat_id={chat_id}&text={msg}')
