from sqlalchemy import select

from app.models.cash_transaction import CashTransaction
from app.repositories.base import BaseRepository


class CashRepository(BaseRepository):
    def list(self, company_id: int) -> list[CashTransaction]:
        stmt = select(CashTransaction).where(CashTransaction.company_id == company_id)
        return list(self.db.scalars(stmt.order_by(CashTransaction.transaction_date.desc())).all())

    def get(self, company_id: int, transaction_id: int) -> CashTransaction | None:
        return self.db.scalar(
            select(CashTransaction).where(
                CashTransaction.company_id == company_id,
                CashTransaction.id == transaction_id,
            )
        )

    def create(self, company_id: int, data: dict) -> CashTransaction:
        tx = CashTransaction(company_id=company_id, **data)
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def update(self, tx: CashTransaction, data: dict) -> CashTransaction:
        for key, value in data.items():
            setattr(tx, key, value)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def delete(self, tx: CashTransaction) -> None:
        self.db.delete(tx)
        self.db.commit()
