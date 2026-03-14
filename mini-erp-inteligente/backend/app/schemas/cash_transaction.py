from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import TimestampSchema


class CashTransactionBase(BaseModel):
    type: str = Field(pattern="^(income|expense)$")
    category: str
    description: str | None = None
    amount: float = Field(gt=0)
    transaction_date: datetime | None = None


class CashTransactionCreate(CashTransactionBase):
    pass


class CashTransactionUpdate(CashTransactionBase):
    pass


class CashTransactionResponse(CashTransactionBase, TimestampSchema):
    id: int
    company_id: int
    transaction_date: datetime
