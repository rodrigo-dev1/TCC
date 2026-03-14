from sqlalchemy import select

from app.models.ai_insight import AIInsight
from app.repositories.base import BaseRepository


class InsightRepository(BaseRepository):
    def list(self, company_id: int) -> list[AIInsight]:
        stmt = select(AIInsight).where(AIInsight.company_id == company_id).order_by(AIInsight.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def create_many(self, insights: list[AIInsight]) -> list[AIInsight]:
        self.db.add_all(insights)
        self.db.commit()
        return insights
