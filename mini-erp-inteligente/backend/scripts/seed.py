from datetime import datetime, timedelta

from sqlalchemy import text

from app.db.session import SessionLocal
from app.models.ai_insight import AIInsight
from app.models.cash_transaction import CashTransaction
from app.models.client import Client
from app.models.company import Company
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.user import User


def run() -> None:
    db = SessionLocal()
    try:
        for table in [
            "sale_items",
            "sales",
            "cash_transactions",
            "ai_insights",
            "clients",
            "products",
            "users",
            "companies",
        ]:
            db.execute(text(f"DELETE FROM {table}"))

        company = Company(name="Loja Exemplo", segment="Varejo")
        db.add(company)
        db.flush()

        user = User(
            company_id=company.id,
            name="Admin",
            email="admin@mini-erp.com",
            google_id="google-admin-1",
            role="owner",
        )
        db.add(user)

        clients = [
            Client(company_id=company.id, name=f"Cliente {i}", email=f"cliente{i}@mail.com", document=f"DOC{i}")
            for i in range(1, 6)
        ]
        db.add_all(clients)

        products = [
            Product(company_id=company.id, name="Produto A", type="product", price=120, stock_quantity=50),
            Product(company_id=company.id, name="Produto B", type="product", price=85, stock_quantity=30),
            Product(company_id=company.id, name="Produto C", type="product", price=45, stock_quantity=80),
            Product(company_id=company.id, name="Produto D", type="product", price=220, stock_quantity=15),
            Product(company_id=company.id, name="Serviço Setup", type="service", price=300, stock_quantity=0),
            Product(company_id=company.id, name="Serviço Suporte", type="service", price=180, stock_quantity=0),
            Product(company_id=company.id, name="Serviço Consultoria", type="service", price=450, stock_quantity=0),
            Product(company_id=company.id, name="Produto E", type="product", price=60, stock_quantity=100),
        ]
        db.add_all(products)
        db.flush()

        sales = []
        sale_items = []
        for i in range(10):
            sale_date = datetime.utcnow() - timedelta(days=i * 3)
            sale = Sale(
                company_id=company.id,
                client_id=clients[i % len(clients)].id,
                payment_method="pix" if i % 2 == 0 else "credit_card",
                status="completed",
                sale_date=sale_date,
                total_amount=0,
            )
            db.add(sale)
            db.flush()

            p1 = products[i % len(products)]
            p2 = products[(i + 1) % len(products)]
            q1, q2 = 1 + (i % 3), 1
            t1, t2 = float(p1.price) * q1, float(p2.price) * q2
            sale_items.extend(
                [
                    SaleItem(sale_id=sale.id, product_id=p1.id, quantity=q1, unit_price=p1.price, total_price=t1),
                    SaleItem(sale_id=sale.id, product_id=p2.id, quantity=q2, unit_price=p2.price, total_price=t2),
                ]
            )
            sale.total_amount = t1 + t2
            sales.append(sale)

        db.add_all(sale_items)

        cash = []
        for i in range(15):
            tx_type = "income" if i % 3 != 0 else "expense"
            amount = 250 + (i * 35)
            cash.append(
                CashTransaction(
                    company_id=company.id,
                    type=tx_type,
                    category="Vendas" if tx_type == "income" else "Operacional",
                    description=f"Movimentação {i+1}",
                    amount=amount,
                    transaction_date=datetime.utcnow() - timedelta(days=i * 2),
                )
            )
        db.add_all(cash)

        insights = [
            AIInsight(
                company_id=company.id,
                type="summary",
                title="Resumo inicial",
                description="O negócio apresenta bom volume de vendas com oportunidades de controle de despesas.",
                severity="low",
                reference_period="30d",
            ),
            AIInsight(
                company_id=company.id,
                type="risk",
                title="Atenção aos custos",
                description="Custos operacionais cresceram na última quinzena.",
                severity="medium",
                reference_period="15d",
            ),
        ]
        db.add_all(insights)
        db.commit()
        print("Seed concluído com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
