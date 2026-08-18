from enum import Enum

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.api.entity.Base import Base


class OrderStatus(Enum):
    PENDING = 0      # 待处理/待支付
    PAID = 1         # 已支付
    SHIPPED = 2      # 配送中
    COMPLETED = 3    # 已完成
    CANCELLED = 4    # 已取消

class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 改成 Integer，默认 0
    position: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'))