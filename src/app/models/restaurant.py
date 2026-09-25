from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.user import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    is_open: Mapped[bool] = mapped_column(nullable=False, default=True)
    opening_hours: Mapped[str] = mapped_column(String(100), nullable=True)
    contact: Mapped[str] = mapped_column(String(50), nullable=True)
