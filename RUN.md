# Running LastBenchIQ on your machine

Three things have to be running: a **database**, the **backend** (API), and the
**frontend** (the pages you see). Open three terminals and keep them open.

---

## Step 0 — the database (once)

The backend needs a PostgreSQL database. The quickest path that also happens to be
the production database later is **Neon** (free, no install):

1. Go to https://neon.com → sign up with Google
2. Create a project, call it `lastbenchiq`
3. Copy the connection string it shows you. It looks like:
   `postgresql://user:pass@ep-xxx.aws.neon.tech/neondb?sslmode=require`
4. Change the start from `postgresql://` to `postgresql+psycopg://`
   (SQLAlchemy needs to know which driver to use — that is all this prefix does)

Now create `backend/.env` (copy `backend/.env.example` and edit it):

```
ENVIRONMENT=local
DEBUG=true
DATABASE_URL=postgresql+psycopg://user:pass@ep-xxx.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=any-long-random-string-for-now
LLM_API_KEY=
```

`.env` is gitignored. It never gets committed, so your database password stays on
your machine.

---

## Step 1 — backend (terminal 1)

```powershell
cd D:\LastBenchIQ\backend
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

`alembic upgrade head` creates the tables. You only need it again when the schema
changes.

Leave `uvicorn` running. Check it works: open http://localhost:8000/docs — you should
see the API with `/auth/register`, `/auth/login`, `/auth/me`.

---

## Step 2 — frontend (terminal 2)

```powershell
cd D:\LastBenchIQ\frontend
npm install
npm run dev
```

Open http://localhost:5173 — it sends you to the sign-in page.

---

## Step 3 — try it

Click **Create one**, fill in your real enrollment number, and sign up. Then:

- refresh the page — you stay signed in
- sign out — you land back on sign-in
- try to open `/` while signed out — it bounces you to sign-in
- sign up again with the same enrollment number — "An account already exists for
  this enrollment number"

---

## Checks before you commit

```powershell
cd D:\LastBenchIQ\backend
ruff check . ; ruff format --check . ; mypy app ; pytest

cd D:\LastBenchIQ\frontend
npm run lint ; npm run typecheck ; npm test
```

The `pytest` run needs the database (the auth tests use a real one).

---

## If something breaks

| What you see | What it means |
|---|---|
| `connection refused` / `could not translate host name` | `DATABASE_URL` is wrong, or you missed `+psycopg` |
| `relation "users" does not exist` | you skipped `alembic upgrade head` |
| frontend loads but sign-in says "Network error" | the backend terminal is not running |
| `py -3.11` not found | Python 3.11 is not installed — 3.13 will fail to build scikit-learn |
