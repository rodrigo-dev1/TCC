from collections import defaultdict
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cash_transaction import CashTransaction
from app.models.client import Client
from app.models.sale import Sale
from app.models.sale_item import SaleItem


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def summary(self, company_id: int) -> dict:
        total_revenue = float(
            self.db.scalar(select(func.coalesce(func.sum(Sale.total_amount), 0)).where(Sale.company_id == company_id))
        )
        total_expenses = float(
            self.db.scalar(
                select(func.coalesce(func.sum(CashTransaction.amount), 0)).where(
                    CashTransaction.company_id == company_id, CashTransaction.type == "expense"
                )
            )
        )
        income_total = float(
            self.db.scalar(
                select(func.coalesce(func.sum(CashTransaction.amount), 0)).where(
                    CashTransaction.company_id == company_id, CashTransaction.type == "income"
                )
            )
        )
        total_sales = int(self.db.scalar(select(func.count(Sale.id)).where(Sale.company_id == company_id)) or 0)
        total_clients = int(self.db.scalar(select(func.count(Client.id)).where(Client.company_id == company_id)) or 0)
        avg_ticket = total_revenue / total_sales if total_sales else 0

        top_rows = self.db.execute(
            select(SaleItem.product_id, func.sum(SaleItem.quantity).label("qty"))
            .join(Sale, Sale.id == SaleItem.sale_id)
            .where(Sale.company_id == company_id)
            .group_by(SaleItem.product_id)
            .order_by(func.sum(SaleItem.quantity).desc())
            .limit(5)
        ).all()

        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "current_balance": income_total - total_expenses,
            "average_ticket": round(avg_ticket, 2),
            "total_clients": total_clients,
            "total_sales": total_sales,
            "top_products": [{"product_id": row.product_id, "quantity": int(row.qty)} for row in top_rows],
        }

    def charts(self, company_id: int) -> dict:
        sales = self.db.scalars(select(Sale).where(Sale.company_id == company_id)).all()
        cash = self.db.scalars(select(CashTransaction).where(CashTransaction.company_id == company_id)).all()
        monthly_rev = defaultdict(float)
        for sale in sales:
            key = sale.sale_date.strftime("%Y-%m")
            monthly_rev[key] += float(sale.total_amount)

        cash_flow = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        for tx in cash:
            key = tx.transaction_date.strftime("%Y-%m")
            cash_flow[key][tx.type] += float(tx.amount)

        return {
            "monthly_revenue": [{"month": k, "revenue": v} for k, v in sorted(monthly_rev.items())],
            "cash_flow": [
                {"month": k, "income": v["income"], "expense": v["expense"]}
                for k, v in sorted(cash_flow.items())
            ],
        }
