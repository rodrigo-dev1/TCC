from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login_google(self, payload: dict) -> dict:
        user = self.repo.get_by_google_id(payload["google_id"])
        if not user:
            user = self.repo.create(
                {
                    "company_id": 1,
                    "name": payload["name"],
                    "email": payload["email"],
                    "google_id": payload["google_id"],
                    "role": "owner",
                }
            )
        token = f"mock-token-{user.id}"
        return {
            "token": token,
            "user": {
                "id": user.id,
                "company_id": user.company_id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            },
        }
