# Mini ERP Inteligente (MVP)

Monorepo com backend FastAPI + frontend React para pequenas empresas, incluindo CRM, produtos/serviços, vendas, caixa, dashboard e insights heurísticos de IA.

## Estrutura

```bash
mini-erp-inteligente/
  backend/
  frontend/
```

## Backend (FastAPI)

### Requisitos
- Python 3.12+
- PostgreSQL 14+

### Execução local
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Crie banco `mini_erp` no PostgreSQL e ajuste `DATABASE_URL`.

### Migrations (Alembic)
```bash
alembic upgrade head
```

### Seed de dados
```bash
PYTHONPATH=. python scripts/seed.py
```

### Rodar API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger: `http://localhost:8000/docs`

## Frontend (React + Vite + Tailwind)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App: `http://localhost:5173`

## Deploy futuro na Google Cloud

- Backend: deploy container no **Cloud Run** (porta 8080, `gunicorn+uvicorn`).
- Frontend: build estático + deploy em **Cloud Run** (Nginx) ou bucket/CDN.
- Banco: **Cloud SQL PostgreSQL**.
- Segredos: guardar credenciais no **Secret Manager**.
- Variáveis de ambiente são carregadas por `.env` local e env vars em produção.

## Login Google (MVP)

Fluxo base implementado com endpoint `/auth/google`. No MVP está com validação simulada (mock) para facilitar desenvolvimento local.

## Seed inicial

- 1 empresa
- 1 usuário
- 5 clientes
- 8 produtos/serviços
- 10 vendas (com itens)
- 15 movimentações de caixa
- insights iniciais
