# Implementation Prompt Template

> Turns one EPIC into 4–6 standalone implementation prompts.
> **Standalone** is the key word: each prompt is handed to a fresh session with no
> memory of the others, so it must carry everything needed to do the work correctly.

---

## Sizing rules

Before running any prompt, size it. Julien's step 7 is explicit about this, and it is
where most AI-assisted builds go wrong.

- **Too vague → split.** "Build the upload feature" is not a prompt. If you cannot list
  the files it will touch, it is too big.
- **Too small → merge.** A prompt that changes one function wastes a session's context.
- **Right size:** one coherent slice, 2–6 files, reviewable in one sitting, independently
  testable.
- **4–6 prompts per EPIC.** More than 6 means the EPIC should have been two EPICs.

A prompt that cannot state its own acceptance criteria is not ready to run.

---

## The template

```markdown
## [EPIC n.m] <short imperative title>

### Context
Read first: `CLAUDE.md`, `docs/KNOWLEDGE_BASE.md`, and <the specific doc sections>.
This is prompt m of k for EPIC n. Already done: <what exists>.

### Goal
<One sentence. What is true after this that was not true before.>

### In scope
- <specific, file-level>

### Out of scope — do NOT build these
- <things a model would reasonably drift into>
- <features from later EPICs>

### Acceptance criteria
- [ ] <checkable, not aspirational>
- [ ] Loading, empty and error states exist (if UI)
- [ ] Works at 375px (if UI)
- [ ] Query filters on `user_id` (if it touches student data)

### Constraints
- Business logic in `services/`, not routers
- No new dependencies without saying why
- `ruff check . && mypy app && pytest` must pass
- (frontend) `npm run lint && npm run typecheck && npm test` must pass

### Done when
<The one observable thing that proves it works.>
```

---

## Standing instruction to append to every prompt

```
Before finishing: run the project's checks and fix what fails. Do not weaken a lint
rule, add `# type: ignore`, or skip a test to go green — if a check fails, the code is
wrong, not the check. If you must deviate from CLAUDE.md, say so explicitly in your
summary rather than doing it quietly.
```

---

# Worked example — EPIC 0 broken into prompts

EPIC 0 is *Walking Skeleton & Real Data*. Step 5's scaffold already delivered the
repo, CI, linting and test layers, so what remains is the database, the deploy, and
measuring what the free tier actually does.

---

## [EPIC 0.1] Wire the database and the first migration

### Context
Read first: `CLAUDE.md`, `docs/DATA_MODEL.md` §1. The scaffold exists: FastAPI app,
`app/models/base.py` with `Base`, `IDMixin`, `TimestampMixin`, `UserOwnedMixin`,
passing CI. There is no database connection yet.

### Goal
The API connects to PostgreSQL, and a first Alembic migration creates the `users` table.

### In scope
- `app/core/db.py` — engine, `SessionLocal`, a `get_db` FastAPI dependency
- `app/models/user.py` — `User` using `Base`, `IDMixin`, `TimestampMixin`
- Alembic initialised and configured to read `DATABASE_URL` from settings
- One migration creating `users`
- `/health/deep` additionally reports database connectivity

### Out of scope — do NOT build these
- Authentication, password hashing, JWT (that is EPIC 1)
- `student_profiles` — **the Kaggle dataset must be chosen first** so its columns are
  derived, not invented
- Any other table

### Acceptance criteria
- [ ] `alembic upgrade head` creates `users` against a local Postgres
- [ ] `alembic downgrade -1` cleanly reverses it
- [ ] `/health/deep` reports `"database": "connected"` or an explicit failure
- [ ] An API test covers the degraded case (database unreachable → reported, not a 500)
- [ ] `ruff check . && mypy app && pytest` pass

### Done when
`docker compose up -d db && alembic upgrade head && curl /api/v1/health/deep` shows the
database connected.

---

## [EPIC 0.2] Containerise and deploy the API

### Context
Read first: `CLAUDE.md`, `docs/TECHNICAL_SPECIFICATION.md` §2, §8. `backend/Dockerfile`
exists and installs Tesseract. Nothing is deployed yet.

### Goal
The API runs on Render against a Neon database, with the full dependency tree installed.

### In scope
- Verify the Docker build locally with the **complete** `requirements.txt`
- Render service configuration (Docker, env vars, health check path)
- Neon database created; migrations run against it
- Deploy steps recorded in `README.md`

### Out of scope
- Any feature endpoint
- Custom domains, CI auto-deploy, monitoring

### Acceptance criteria
- [ ] Docker image builds with sklearn, pandas, PyMuPDF, pytesseract **and Tesseract**
- [ ] The build-time verification line in the Dockerfile passes
- [ ] Deployed `/api/v1/health/deep` returns `status: "ok"` — every package `true`,
      Tesseract found
- [ ] `alembic upgrade head` has run against Neon
- [ ] No secret is committed; all config is Render env vars

### Done when
The public `/health/deep` URL returns `"status": "ok"` with no missing dependency.

> **This is the single most valuable prompt in EPIC 0.** If the dependency tree does not
> fit the free tier, this is where you find out — in week 1, with time to change host or
> trim dependencies, instead of in week 7.

---

## [EPIC 0.3] Deploy the frontend and prove the round-trip

### Context
Read first: `CLAUDE.md`. `ApiStatus.tsx` already calls `/api/v1/health`. The dev server
proxies `/api` to localhost:8000, which does not exist in production.

### Goal
The deployed React app reaches the deployed API.

### In scope
- `VITE_API_BASE_URL` env var; `src/api/client.ts` uses it with the proxy as local default
- Vercel project configured and deployed
- Backend CORS updated to allow the Vercel origin

### Out of scope
- Routing, auth screens, layout work, any feature UI

### Acceptance criteria
- [ ] Deployed site shows "API connected"
- [ ] No CORS errors in the browser console
- [ ] Local `npm run dev` still works unchanged
- [ ] `npm run lint && npm run typecheck && npm test` pass

### Done when
Opening the Vercel URL on a phone shows "API connected".

---

## [EPIC 0.4] Measure what the free tier actually does

### Context
Read first: `docs/KNOWLEDGE_BASE.md` §5. Everything is deployed. The plan assumes
things about cold starts, memory, and rate limits that have not been measured.

### Goal
Replace assumptions with numbers, written into `KNOWLEDGE_BASE.md`.

### In scope
- Measure: cold-start time after idle, memory headroom under load, Groq's real
  rate limit and token cap, time to process one 20-question paper end to end
- A small script under `backend/scripts/` that can be re-run later
- Record every number in `KNOWLEDGE_BASE.md` §6

### Out of scope
- Optimising anything. This prompt measures; it does not fix.

### Acceptance criteria
- [ ] Cold-start time measured and recorded
- [ ] Memory headroom recorded with the full dependency tree loaded
- [ ] Groq rate limit and daily cap recorded from a real 429, not from docs
- [ ] Each number is compared against the NFR it affects, and any violated NFR is
      flagged in `KNOWLEDGE_BASE.md`

### Done when
`KNOWLEDGE_BASE.md` §6 contains real measurements, and any assumption they break is
written down as a decision to revisit.

---

## [EPIC 0.5] Collect real question papers — manual, no prompt

**Not an AI task.** This is the highest-leverage hour of the whole project and it needs
a human with a phone.

- [ ] **10–15 real papers**, across **≥2 subjects**
- [ ] A deliberate mix: clean PDFs *and* bad phone photos — skewed, shadowed, creased.
      **The bad ones matter most**, because that is what students will actually upload
- [ ] At least 2 with marks printed in the margin, and at least 2 where marks are hard
      to read
- [ ] Saved to `ml/data/raw_papers/` (gitignored), named `<subject>_<year>_<type>.<ext>`
- [ ] A short `ml/data/raw_papers/INVENTORY.md`: what each file is and how clean it is

> Risk #1 — question segmentation — cannot be built or benchmarked without these.
> Collect them before writing EPIC 2 or 3 code. Everything downstream is guesswork
> until they exist.
