from pydantic import BaseModel, Field

from app.schemas.common import TimestampSchema


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    type: str = Field(default="product", pattern="^(product|service)$")
    price: float = Field(ge=0)
    stock_quantity: int | None = 0
    active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase, TimestampSchema):
    id: int
    company_id: int
