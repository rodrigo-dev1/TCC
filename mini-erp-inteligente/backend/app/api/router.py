from fastapi import APIRouter

from app.api.endpoints import (
    auth,
    cash_transactions,
    clients,
    company,
    dashboard,
    health,
    insights,
    products,
    sales,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(company.router)
api_router.include_router(clients.router)
api_router.include_router(products.router)
api_router.include_router(sales.router)
api_router.include_router(cash_transactions.router)
api_router.include_router(dashboard.router)
api_router.include_router(insights.router)
