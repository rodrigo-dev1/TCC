from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(20), default="product")
    price: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    stock_quantity: Mapped[int | None] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    company = relationship("Company", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")
