from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai_insight import AIInsight
from app.models.cash_transaction import CashTransaction
from app.models.sale import Sale


class AIService:
    def __init__(self, db: Session):
        self.db = db

    def generate_insights(self, company_id: int) -> list[AIInsight]:
        now = datetime.utcnow()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        prev_month_start = (current_month_start - timedelta(days=1)).replace(day=1)

        sales = self.db.scalars(select(Sale).where(Sale.company_id == company_id)).all()
        cash = self.db.scalars(select(CashTransaction).where(CashTransaction.company_id == company_id)).all()

        revenue_total = sum(float(s.total_amount) for s in sales)
        expenses_total = sum(float(c.amount) for c in cash if c.type == "expense")
        income_total = sum(float(c.amount) for c in cash if c.type == "income")

        current_month_revenue = sum(float(s.total_amount) for s in sales if s.sale_date >= current_month_start)
        previous_month_revenue = sum(
            float(s.total_amount) for s in sales if prev_month_start <= s.sale_date < current_month_start
        )

        insights: list[AIInsight] = [
            AIInsight(
                company_id=company_id,
                type="summary",
                title="Resumo financeiro",
                description=(
                    f"Receita total de R$ {revenue_total:.2f}, despesas de R$ {expenses_total:.2f} "
                    f"e saldo de caixa de R$ {income_total - expenses_total:.2f}."
                ),
                severity="low",
                reference_period="30d",
            )
        ]

        if revenue_total > 0 and expenses_total / revenue_total > 0.7:
            insights.append(
                AIInsight(
                    company_id=company_id,
                    type="risk",
                    title="Despesas elevadas",
                    description="As despesas estão acima de 70% da receita. Reavalie custos fixos e margens.",
                    severity="high",
                    reference_period="30d",
                )
            )

        if previous_month_revenue > 0 and current_month_revenue < previous_month_revenue * 0.85:
            insights.append(
                AIInsight(
                    company_id=company_id,
                    type="risk",
                    title="Queda de faturamento",
                    description="O faturamento do mês atual caiu mais de 15% em relação ao mês anterior.",
                    severity="medium",
                    reference_period="monthly",
                )
            )

        avg_daily_net = (income_total - expenses_total) / 30 if cash else 0
        projected_30d = (income_total - expenses_total) + avg_daily_net * 30
        severity = "high" if projected_30d < 0 else "medium"
        insights.append(
            AIInsight(
                company_id=company_id,
                type="forecast",
                title="Previsão de fluxo de caixa (30 dias)",
                description=(
                    f"Com base na média histórica, o saldo projetado para 30 dias é R$ {projected_30d:.2f}."
                ),
                severity=severity,
                reference_period="30d",
            )
        )

        insights.append(
            AIInsight(
                company_id=company_id,
                type="action",
                title="Sugestão de ação",
                description="Priorize produtos com maior giro e faça campanhas para clientes inativos no último mês.",
                severity="low",
                reference_period="next_30d",
            )
        )
        return insights
