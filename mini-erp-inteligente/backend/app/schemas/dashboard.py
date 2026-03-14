from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_revenue: float
    total_expenses: float
    current_balance: float
    average_ticket: float
    total_clients: int
    total_sales: int
    top_products: list[dict]


class DashboardCharts(BaseModel):
    monthly_revenue: list[dict]
    cash_flow: list[dict]
