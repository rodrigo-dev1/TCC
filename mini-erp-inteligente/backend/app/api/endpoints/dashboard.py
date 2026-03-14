from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.dashboard import DashboardCharts, DashboardSummary
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return DashboardService(db).summary(current_user["company_id"])


@router.get("/charts", response_model=DashboardCharts)
def charts(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return DashboardService(db).charts(current_user["company_id"])
