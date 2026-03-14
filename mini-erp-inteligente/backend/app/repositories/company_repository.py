from sqlalchemy import select

from app.models.company import Company
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository):
    def get(self, company_id: int) -> Company | None:
        return self.db.scalar(select(Company).where(Company.id == company_id))

    def update(self, company: Company, data: dict) -> Company:
        for key, value in data.items():
            setattr(company, key, value)
        self.db.commit()
        self.db.refresh(company)
        return company
