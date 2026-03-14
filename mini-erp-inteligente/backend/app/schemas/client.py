from pydantic import BaseModel, EmailStr

from app.schemas.common import TimestampSchema


class ClientBase(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    document: str | None = None
    notes: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientResponse(ClientBase, TimestampSchema):
    id: int
    company_id: int
