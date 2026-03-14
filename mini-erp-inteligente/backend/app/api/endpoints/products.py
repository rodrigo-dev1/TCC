from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return ProductRepository(db).list(current_user["company_id"])


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = ProductRepository(db).get(current_user["company_id"], product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto/serviço não encontrado")
    return product


@router.post("", response_model=ProductResponse)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return ProductRepository(db).create(current_user["company_id"], payload.model_dump())


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = ProductRepository(db)
    product = repo.get(current_user["company_id"], product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto/serviço não encontrado")
    return repo.update(product, payload.model_dump())


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    repo = ProductRepository(db)
    product = repo.get(current_user["company_id"], product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto/serviço não encontrado")
    repo.delete(product)
    return {"message": "Produto removido"}
