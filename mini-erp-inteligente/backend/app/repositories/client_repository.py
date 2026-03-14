from sqlalchemy import or_, select

from app.models.client import Client
from app.repositories.base import BaseRepository


class ClientRepository(BaseRepository):
    def list(self, company_id: int, search: str | None = None) -> list[Client]:
        stmt = select(Client).where(Client.company_id == company_id)
        if search:
            token = f"%{search}%"
            stmt = stmt.where(
                or_(Client.name.ilike(token), Client.email.ilike(token), Client.document.ilike(token))
            )
        return list(self.db.scalars(stmt.order_by(Client.name)).all())

    def get(self, company_id: int, client_id: int) -> Client | None:
        return self.db.scalar(select(Client).where(Client.company_id == company_id, Client.id == client_id))

    def create(self, company_id: int, data: dict) -> Client:
        client = Client(company_id=company_id, **data)
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update(self, client: Client, data: dict) -> Client:
        for key, value in data.items():
            setattr(client, key, value)
        self.db.commit()
        self.db.refresh(client)
        return client

    def delete(self, client: Client) -> None:
        self.db.delete(client)
        self.db.commit()
