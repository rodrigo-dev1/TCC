from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.cash_repository import CashRepository
from app.schemas.cash_transaction import (
    CashTransactionCreate,
    CashTransactionResponse,
    CashTransactionUpdate,
)

router = APIRouter(prefix="/cash-transactions", tags=["cash-transactions"])


@router.get("", response_model=list[CashTransactionResponse])
def list_transactions(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return CashRepository(db).list(current_user["company_id"])


@router.get("/{transaction_id}", response_model=CashTransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tx = CashRepository(db).get(current_user["company_id"], transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    return tx


@router.post("", response_model=CashTransactionResponse)
def create_transaction(
    payload: CashTransactionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    data = payload.model_dump()
    data["transaction_date"] = data.get("transaction_date") or datetime.utcnow()
    return CashRepository(db).create(current_user["company_id"], data)


@router.put("/{transaction_id}", response_model=CashTransactionResponse)
def update_transaction(
    transaction_id: int,
    payload: CashTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = CashRepository(db)
    tx = repo.get(current_user["company_id"], transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    data = payload.model_dump()
    data["transaction_date"] = data.get("transaction_date") or tx.transaction_date
    return repo.update(tx, data)


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    repo = CashRepository(db)
    tx = repo.get(current_user["company_id"], transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    repo.delete(tx)
    return {"message": "Movimentação removida"}
