# Real-Time QA Test Execution Dashboard

A full-stack dashboard for managing test cases, recording test executions, tracking defects, and monitoring regression-cycle health.

## Stack

- API: Python, FastAPI, SQLAlchemy
- UI: React, TypeScript, Vite
- Database: PostgreSQL (SQLite is used automatically for local development)
- Automation: Playwright and GitHub Actions

## Run locally

### API

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`; documentation is at `/docs`.

### Dashboard

```powershell
cd frontend
npm install
npm run dev
```

## PostgreSQL

Set `DATABASE_URL` before starting the API:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://qa_user:qa_password@localhost:5432/qa_dashboard"
```

`docker-compose.yml` supplies the matching local database configuration.

## API

- `GET/POST /api/test-cases`
- `GET/POST /api/executions`
- `GET/POST /api/defects`
- `GET /api/dashboard/summary`
