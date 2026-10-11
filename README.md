# LastBenchIQ

An AI companion for final-year college students: upload past exam papers, get a
prioritised study plan, and a career roadmap built by an agent.

Planning documents live in [`docs/`](docs/) and are the source of truth.
Read them in order: `PRODUCT_DESCRIPTION` → `TECHNICAL_SPECIFICATION` →
`DATA_MODEL` / `API_CONTRACTS` → `AUDIT_RESPONSE` → `EPICS`.

## Stack

React + Vite + Tailwind · FastAPI + SQLAlchemy · PostgreSQL · scikit-learn

## Quick start

```bash
# 1. database
docker compose up -d db

# 2. backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env            # then set SECRET_KEY
uvicorn app.main:app --reload   # http://localhost:8000/docs

# 3. frontend
cd ../frontend
npm install
npm run dev                     # http://localhost:5173
```

Open `http://localhost:8000/api/v1/health/deep` — it reports whether the heavy
dependencies and the Tesseract binary are actually present. Check it after every
deploy; a `degraded` status there is the early warning that OCR will fail later.

## Checks

These run in CI on every push and must pass before merge.

| Layer | Command |
|---|---|
| Lint (Python) | `cd backend && ruff check .` |
| Format (Python) | `cd backend && ruff format --check .` |
| Types (Python, strict) | `cd backend && mypy app` |
| Unit + API tests | `cd backend && pytest` |
| Lint (TS) | `cd frontend && npm run lint` |
| Types (TS, strict) | `cd frontend && npm run typecheck` |
| Component tests | `cd frontend && npm test` |
| End-to-end | `cd frontend && npm run test:e2e` |

> **Do not weaken a rule to make CI pass.** The strictness is the mechanism that
> validates generated code automatically. A failing check is information.

## Layout

```
backend/app/    api · services · models · schemas · agents · core
backend/tests/  unit · api
frontend/src/   pages · components · api
frontend/e2e/   Playwright specs
ml/             notebooks · data (gitignored) · models
docs/           planning documents
```

**Rule:** business logic lives in `backend/app/services/`, never in routers.
Routers validate and delegate.

## Deployment

The backend ships as a container because **Tesseract is a system binary, not a pip
package** — see `backend/Dockerfile`. The build verifies it is present rather than
discovering it is missing in production.

| Tier | Host | Config |
|---|---|---|
| Database | Neon (free) | copy the connection string into Render's `DATABASE_URL` |
| API | Render (free, Docker) | `render.yaml` — New → Blueprint |
| Web | Vercel (free) | `vercel.json`; set `VITE_API_BASE_URL` to the Render URL |

After deploying, run the measurement script before building any feature:

```bash
python backend/scripts/measure_free_tier.py --url https://<your-api>.onrender.com
```

It checks that every heavy dependency, the Tesseract binary and the database are
actually present, then measures latency against the NFRs. **A `degraded` result
means the free tier cannot carry this dependency tree — find that out now, not in
week 7.** Record the numbers in `docs/KNOWLEDGE_BASE.md` §6.
