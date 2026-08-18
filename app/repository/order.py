from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.entity.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_orders_by_user_id(self, user_id: int) -> list[Order]:
        sql = text(
            "SELECT id, number, status, position, user_id "
            "FROM `order` WHERE user_id = :user_id ORDER BY id DESC"
        )

        result = await self.session.execute(sql, {"user_id": user_id})
        rows = result.mappings().fetchall()

        return [
            Order(
                number=row["number"],
                id=row["id"],
                status=row["status"],
                position=row["position"],
                user_id=row["user_id"]
            ) for row in rows
        ]

    async def get_order_by_number(self, order_num: str, user_id: int) -> Order | None:
        sql = text(
            "SELECT id, number, status, position, user_id "
            "FROM `order` WHERE number = :number AND user_id = :user_id"
        )

        result = await self.session.execute(sql, {"number": order_num, "user_id": user_id})

        row = result.mappings().first()
        if not row:
            return None

        return Order(
            id=row["id"],
            number=row["number"],
            status=row["status"],
            position=row["position"],
            user_id=row["user_id"],
        )
