from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.ai_insight import AIInsight
from app.repositories.insight_repository import InsightRepository
from app.schemas.insight import AIInsightResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("", response_model=list[AIInsightResponse])
def list_insights(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return InsightRepository(db).list(current_user["company_id"])


@router.post("/generate", response_model=list[AIInsightResponse])
def generate_insights(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    generated: list[AIInsight] = AIService(db).generate_insights(current_user["company_id"])
    return InsightRepository(db).create_many(generated)
