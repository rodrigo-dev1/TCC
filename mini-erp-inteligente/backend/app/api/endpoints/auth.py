from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, GoogleAuthRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=AuthResponse)
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    return service.login_google(payload.model_dump())


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user
