from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    segment: Mapped[str] = mapped_column(String(120), default="General")

    users = relationship("User", back_populates="company")
    clients = relationship("Client", back_populates="company")
    products = relationship("Product", back_populates="company")
    sales = relationship("Sale", back_populates="company")
    cash_transactions = relationship("CashTransaction", back_populates="company")
    insights = relationship("AIInsight", back_populates="company")
