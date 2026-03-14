from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.repositories.base import BaseRepository


class SaleRepository(BaseRepository):
    def list(self, company_id: int) -> list[Sale]:
        stmt = (
            select(Sale)
            .where(Sale.company_id == company_id)
            .options(selectinload(Sale.items))
            .order_by(Sale.sale_date.desc())
        )
        return list(self.db.scalars(stmt).all())

    def get(self, company_id: int, sale_id: int) -> Sale | None:
        stmt = (
            select(Sale)
            .where(Sale.company_id == company_id, Sale.id == sale_id)
            .options(selectinload(Sale.items))
        )
        return self.db.scalar(stmt)

    def create_sale(self, sale: Sale, items: list[SaleItem]) -> Sale:
        self.db.add(sale)
        self.db.flush()
        for item in items:
            item.sale_id = sale.id
            self.db.add(item)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def replace_items(self, sale: Sale, items: list[SaleItem]) -> Sale:
        sale.items.clear()
        self.db.flush()
        for item in items:
            sale.items.append(item)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def delete(self, sale: Sale) -> None:
        self.db.delete(sale)
        self.db.commit()
