from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import TimestampSchema


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class SaleItemResponse(BaseModel):
    id: int
    sale_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float

    model_config = {"from_attributes": True}


class SaleCreate(BaseModel):
    client_id: int | None = None
    payment_method: str = "pix"
    status: str = "completed"
    sale_date: datetime | None = None
    items: list[SaleItemCreate]


class SaleUpdate(SaleCreate):
    pass


class SaleResponse(TimestampSchema):
    id: int
    company_id: int
    client_id: int | None
    total_amount: float
    payment_method: str
    status: str
    sale_date: datetime
    items: list[SaleItemResponse]
