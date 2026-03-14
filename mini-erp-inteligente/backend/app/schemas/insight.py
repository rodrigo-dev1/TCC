from app.schemas.common import TimestampSchema


class AIInsightResponse(TimestampSchema):
    id: int
    company_id: int
    type: str
    title: str
    description: str
    severity: str
    reference_period: str
