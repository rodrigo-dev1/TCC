from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.sale_repository import SaleRepository
from app.schemas.sale import SaleCreate, SaleResponse, SaleUpdate
from app.services.sale_service import SaleService

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("", response_model=list[SaleResponse])
def list_sales(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return SaleRepository(db).list(current_user["company_id"])


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sale = SaleRepository(db).get(current_user["company_id"], sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale


@router.post("", response_model=SaleResponse)
def create_sale(payload: SaleCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return SaleService(db).create(current_user["company_id"], payload.model_dump())


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: int,
    payload: SaleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return SaleService(db).update(current_user["company_id"], sale_id, payload.model_dump())


@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    repo = SaleRepository(db)
    sale = repo.get(current_user["company_id"], sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    repo.delete(sale)
    return {"message": "Venda removida"}
