from pydantic import BaseModel, EmailStr


class GoogleAuthRequest(BaseModel):
    google_id: str
    email: EmailStr
    name: str


class AuthResponse(BaseModel):
    token: str
    user: dict
