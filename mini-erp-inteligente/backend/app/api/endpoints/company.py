from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyResponse, CompanyUpdate

router = APIRouter(prefix="/company", tags=["company"])


@router.get("", response_model=CompanyResponse)
def get_company(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    company = CompanyRepository(db).get(current_user["company_id"])
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return company


@router.put("", response_model=CompanyResponse)
def update_company(
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = CompanyRepository(db)
    company = repo.get(current_user["company_id"])
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return repo.update(company, payload.model_dump())
