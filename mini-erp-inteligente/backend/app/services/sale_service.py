from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.repositories.product_repository import ProductRepository
from app.repositories.sale_repository import SaleRepository


class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)
        self.product_repo = ProductRepository(db)

    def _build_items(self, company_id: int, items_data: list[dict]) -> tuple[list[SaleItem], float]:
        items = []
        total = 0.0
        for item_data in items_data:
            product = self.product_repo.get(company_id, item_data["product_id"])
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
            qty = item_data["quantity"]
            unit_price = float(product.price)
            total_price = unit_price * qty
            items.append(
                SaleItem(
                    product_id=product.id,
                    quantity=qty,
                    unit_price=unit_price,
                    total_price=total_price,
                )
            )
            total += total_price
        return items, total

    def create(self, company_id: int, data: dict) -> Sale:
        items, total = self._build_items(company_id, data["items"])
        sale = Sale(
            company_id=company_id,
            client_id=data.get("client_id"),
            payment_method=data.get("payment_method", "pix"),
            status=data.get("status", "completed"),
            sale_date=data.get("sale_date") or datetime.utcnow(),
            total_amount=total,
        )
        return self.sale_repo.create_sale(sale, items)

    def update(self, company_id: int, sale_id: int, data: dict) -> Sale:
        sale = self.sale_repo.get(company_id, sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        items, total = self._build_items(company_id, data["items"])
        sale.client_id = data.get("client_id")
        sale.payment_method = data.get("payment_method", sale.payment_method)
        sale.status = data.get("status", sale.status)
        sale.sale_date = data.get("sale_date") or sale.sale_date
        sale.total_amount = total
        return self.sale_repo.replace_items(sale, items)
