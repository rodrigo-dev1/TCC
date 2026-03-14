from datetime import datetime

from pydantic import BaseModel


class ORMBase(BaseModel):
    model_config = {"from_attributes": True}


class TimestampSchema(ORMBase):
    created_at: datetime
    updated_at: datetime
