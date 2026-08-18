from dataclasses import dataclass

from app.api.entity.order import Order
from app.repository.order import OrderRepository

STATUS_TEXT = {
    0: "待支付",
    1: "已支付",
    2: "配送中",
    3: "已完成",
    4: "已取消",
}


@dataclass
class OrderInfo:
    order_num: str
    status: int
    status_text: str
    position: str


class OrderService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    @staticmethod
    def _to_info(order: Order) -> OrderInfo:
        return OrderInfo(
            order_num=order.number,
            status=order.status,
            status_text=STATUS_TEXT.get(order.status, "未知"),
            position=order.position,
        )

    async def get_orders(self, user_id: int) -> list[OrderInfo]:
        orders = await self.order_repository.get_orders_by_user_id(user_id)
        return [self._to_info(order) for order in orders]

    async def get_order(self, order_num: str, user_id: int) -> OrderInfo | None:
        order = await self.order_repository.get_order_by_number(order_num, user_id)
        if not order:
            return None
        
        return self._to_info(order)
