from pydantic import BaseModel

from app.schemas.common import TimestampSchema


class CompanyResponse(TimestampSchema):
    id: int
    name: str
    segment: str


class CompanyUpdate(BaseModel):
    name: str
    segment: str
