from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repository import UserRepository


def get_current_user(
    db: Session = Depends(get_db),
    x_user_id: int | None = Header(default=1, alias="X-User-Id"),
) -> dict:
    user = UserRepository(db).get_by_id(x_user_id or 1)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return {
        "id": user.id,
        "company_id": user.company_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }
