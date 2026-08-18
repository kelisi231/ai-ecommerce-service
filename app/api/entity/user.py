from app.api.entity.Base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
