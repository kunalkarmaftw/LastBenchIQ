# CLAUDE.md — working rules for this repository

Read this before writing any code here. It encodes decisions that were argued out
already; re-opening them costs time the project does not have.

If a rule here conflicts with something you believe is better practice: the rule
wins, or you raise it explicitly and get it changed here first. Do not quietly
deviate.

---

## What this is

**LastBenchIQ** — an AI study and career companion for final-year college students.
Upload past exam papers → get topics ranked by what actually carries marks. State a
career goal → an agent builds a roadmap.

Solo developer, ~8 weeks, hard November deadline, student budget (free tiers only).
It must satisfy an academic examiner *and* be good enough that real students use it.

**Source of truth is `docs/`.** Read in this order:
`PRODUCT_DESCRIPTION` → `TECHNICAL_SPECIFICATION` → `DATA_MODEL` / `API_CONTRACTS`
→ `AUDIT_RESPONSE` → `EPICS` → `KNOWLEDGE_BASE`.

---

## Non-negotiable rules

### 1. Business logic lives in `backend/app/services/`
Routers validate input and delegate. A router containing a loop, an LLM call, or a
database query beyond a simple fetch is wrong. This keeps logic testable without an
HTTP client, and explainable in a viva.

### 2. Every user-owned table uses `UserOwnedMixin`
Never add a table holding student data without it. Never write a query against such a
table without filtering on `user_id`. Routes take bare UUIDs, so an unfiltered query
leaks another student's data. This was a real finding in the Step 3 audit.

### 3. Do not add these dependencies
| Banned | Why |
|---|---|
| **LangChain** (for the agent loop) | Hides the plan→act→observe→re-plan loop that must be explained in the viva. The loop is ~150 lines written by hand. |
| **torch / sentence-transformers** | ~400MB+. Will OOM the 512MB free tier. |
| **ChromaDB / any vector store** | Nothing in P0/P1 uses RAG. If retrieval becomes necessary, use a hosted embedding API. |
| **Celery / Redis** | Ops overhead for a solo build. Use FastAPI `BackgroundTasks`. |

### 4. Agent loops are always bounded
`MAX_ITERATIONS` and a wall-clock timeout, read from settings. Every step persisted to
`agent_steps`. An unbounded loop is a hang and a bill.

### 5. Never weaken a check to make CI pass
ruff, mypy strict, eslint, tsc strict. If a check fails, fix the code. Adding `# noqa`,
`# type: ignore`, or `eslint-disable` requires a comment saying *why*, and it should be
rare. The strictness is what validates generated code so a human doesn't have to read
every line.

### 6. Honest labels
Only the Career Planning Agent gets called **"agentic"** — it has a real
plan/act/observe/re-plan loop with tools. Everything else is **"AI-powered"**. The
Adaptive Interviewer is **"adaptive"**, not agentic. Never claim a metric a model cannot
produce (K-Means has no confusion matrix — it is unsupervised).

### 7. Three UI states, always
Every screen handles **loading**, **empty**, and **error** — not just the happy path. The
empty state matters most: a brand-new user has uploaded nothing, and that is the first
thing they see.

### 8. Mobile is the real target
A student on a phone at 11pm. Must work at 375px. No horizontal scroll.

---

## Stack

| | |
|---|---|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL |
| Frontend | React 18, Vite, TypeScript (strict), Tailwind, React Query, Recharts |
| ML | scikit-learn, pandas, joblib — trained in `ml/notebooks/`, served from `.pkl` |
| LLM | Groq (Llama), behind a thin function — not an abstraction layer |
| Docs/OCR | PyMuPDF → Tesseract → vision LLM (tiered, in that order) |
| Deploy | Vercel (web) · Render via Docker (API) · Neon (DB) |

---

## Layout

```
backend/app/
  api/        routers — validate and delegate, nothing more
  services/   business logic lives here
  agents/     agent loop, tools, prompts
  models/     SQLAlchemy models (use the mixins in models/base.py)
  schemas/    Pydantic request/response models
  core/       config, db, security
backend/tests/   unit/ (no DB) · api/ (through TestClient)
frontend/src/    pages/ components/ api/
frontend/e2e/    Playwright
ml/              notebooks/ data/ (gitignored) models/
docs/            planning documents — the source of truth
```

---

## Commands

```bash
# backend
cd backend
ruff check . && ruff format --check . && mypy app && pytest

# frontend
cd frontend
npm run lint && npm run typecheck && npm test && npm run build
npm run test:e2e
```

All of these run in CI on every push. Run them locally before committing.

---

## Conventions

- **Naming:** `snake_case` Python, `camelCase` TS, `PascalCase` components
- **Types:** no bare `dict`/`Any` in signatures; no `any` in TypeScript
- **Errors:** API returns `{"detail": str, "code": str}`; never leak stack traces
- **Secrets:** `.env` only, never committed; config via `app/core/config.py`
- **Async:** FastAPI endpoints `async` only when doing real I/O concurrently; a sync
  endpoint is fine and simpler
- **Tests:** mark `@pytest.mark.unit` or `@pytest.mark.api`
- **Commits:** imperative mood, say *why* not *what*

---

## Degradation rules (do not silently fail)

| Situation | Behaviour |
|---|---|
| < 3 papers or < 50 questions | Return `insufficient_data` with a call to action — **never cluster anyway** |
| Marks unparseable | `scoring_mode: "frequency_only"`, and wording changes from *"% of marks"* to *"% of questions"* |
| Profile incomplete | Agent asks the student to complete it — **never predicts from nulls** |
| LLM rate-limited | Back off, show a human message, keep cached results usable |
| A tool fails mid-agent-run | Agent observes the failure and re-plans; it does not hang |
| **No past papers for a subject** | State the limit plainly. Offer syllabus structure, teaching-hour weighting and generated practice. **Never invent a ranking**, and never borrow another subject's questions to fake one |
| Page is a scan with a text layer | Distrust the text. Image coverage > 80% means scan (`FINDINGS_EXTRACTION §2`) |
| Uploaded paper's course code mismatches the subject | Warn the student; do not silently mix it into ranking |

Reporting a marks percentage computed from missing marks is the product lying to a
student the night before an exam. Degrade visibly.

---

## Caching rule

Revision notes are cached **per topic, not per user**. Thirty students revising the
same topic must not cost thirty LLM calls — that is exactly the night the free tier
runs out.

---

## When you are blocked

1. Check `docs/KNOWLEDGE_BASE.md` — it records gotchas already hit
2. Check whether the docs already decided it
3. If genuinely undecided: ask, or pick the simpler option and write the decision into
   `KNOWLEDGE_BASE.md`
4. **Do not** invent a feature, a table, or a dependency that no document mentions

---

## What matters most

The project is judged on a working demo and an honest report. A feature that demos well
but no student would open on a real exam night is a failed feature. Depth over count —
two things that genuinely work beat seven half-built ones.
