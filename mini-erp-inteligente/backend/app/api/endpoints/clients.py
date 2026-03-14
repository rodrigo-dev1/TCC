from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientResponse])
def list_clients(search: str | None = None, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return ClientRepository(db).list(current_user["company_id"], search)


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = ClientRepository(db).get(current_user["company_id"], client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.post("", response_model=ClientResponse)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return ClientRepository(db).create(current_user["company_id"], payload.model_dump())


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    payload: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = ClientRepository(db)
    client = repo.get(current_user["company_id"], client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return repo.update(client, payload.model_dump())


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    repo = ClientRepository(db)
    client = repo.get(current_user["company_id"], client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    repo.delete(client)
    return {"message": "Cliente removido"}
