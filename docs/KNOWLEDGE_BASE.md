# LastBenchIQ — Knowledge Base

> A condensed, living summary. Read this to get current fast; update it whenever a
> decision is made or a gotcha is discovered, so future sessions start with less
> ambiguity rather than re-deriving the same conclusions.

**Last updated:** 2026-10-11 · after Step 5 (scaffold)

---

## 1. One-paragraph summary

LastBenchIQ turns a student's own past exam papers into a prioritised study plan, and
their career goal into an agent-built roadmap. The claim is not "many AI features" — it
is that **the pieces are connected and it remembers you**: PYQ → topics → notes, and
resume → gaps → roadmap → interview → back to gaps, with nothing re-typed by the
student. Solo build, 8 weeks, November deadline.

---

## 2. Decisions already made — do not re-litigate

| Decision | Reason |
|---|---|
| React + FastAPI + PostgreSQL | One language for API and ML; React survives real student use where Streamlit would not |
| **Agent loop written by hand, no LangChain** | The loop must be explainable line by line in a viva; LangChain hides it and its API churns |
| **No vector store / RAG in v1** | Nothing in P0/P1 uses it, and torch would OOM the free tier |
| **No Celery/Redis** | FastAPI `BackgroundTasks` is sufficient at this scale |
| Web Speech API over Whisper | Free and low-latency. **Caveat: Chrome sends audio to Google** — must be disclosed |
| Tiered OCR (PDF text → Tesseract → vision LLM) | Students photograph papers with phones; Tesseract alone degrades badly on that |
| Both ML models are P0 | Classical ML is a pass/fail academic requirement; it cannot sit in a band that can slip |
| `user_id` denormalised onto child tables | Routes take bare UUIDs; a missed join would leak another student's data |
| Resume Analyzer + Interviewer kept despite audit advice | Deliberate override — see `AUDIT_RESPONSE §5`; protected by cut triggers instead |

---

## 3. The three intelligence layers (the project's technical argument)

| Layer | Tech | Used for |
|---|---|---|
| **Classical ML** | scikit-learn | Prediction & ranking — question classification, placement probability, topic clustering |
| **Generative AI** | LLM | Generation — revision notes, topic naming, segmentation |
| **Agentic AI** | Hand-built loop + tools | Autonomous multi-step work — career planning |

**The integration proof:** the Career Agent calls `predict_placement` — the classical ML
model — as a *tool*, and the reasoning trace shows it happening. That one screen answers
both *"where is the agentic AI?"* and *"is the ML bolted on?"*

---

## 4. The ML story (what makes it genuine)

Three models, and the ordering matters:

1. **Question Classifier** ★ — supervised, trained on **300–500 questions we hand-label
   ourselves** from real collected papers. Train/test `split` fixed at labelling time.
   Real confusion matrix, real per-class F1. *This is the headline, because it is our own
   dataset, and it sits inside the P0 pipeline.*
2. **Placement Predictor** — Logistic Regression vs Random Forest on a public Kaggle
   campus-placement dataset. Called by the agent as a tool.
3. **Topic Clusterer** — TF-IDF + K-Means. **Unsupervised: silhouette, inertia, elbow —
   no confusion matrix exists for it.**

> **Build rule:** choose the Kaggle dataset *before* writing `student_profiles`, and
> derive the columns from its column list. The reverse order is what originally produced
> an API asking for fields no table had.

---

## 5. Risks, ranked

1. **Question segmentation** — turning raw text into `(question, marks, year)` across
   arbitrary paper formats. Harder than the OCR feeding it, and everything downstream
   depends on it. *Mitigation: collect 10–15 real papers first; LLM-based segmenter as
   the primary path; a manual-correction screen as the escape hatch.*
2. **Free-tier deployment** — 500MB+ deps, Tesseract as a system binary, cold starts,
   rate limits, background tasks lost on spin-down. *Mitigation: EPIC 0 deploys a
   hello-world with the full dependency tree in week 1.*
3. **Scope** — ~205h of plan against ~125h at a normal pace. *Mitigation: cut triggers
   agreed in advance (`AUDIT_RESPONSE §6`).*

---

## 6. Gotchas discovered so far

| Gotcha | Resolution |
|---|---|
| ruff `S105` flags the dev secret default | Extracted to `DEV_SECRET_SENTINEL` with one reviewed `noqa`; `validate_production()` refuses to start with it |
| mypy strict: mixins can't see `__tablename__` | Declared `__tablename__: ClassVar[str]` on `UserOwnedMixin` |
| eslint strict bans `getElementById(...)!` | Check for null and throw a real error instead |
| Playwright may not match a preinstalled browser build | `CHROMIUM_PATH` env var overrides `executablePath`; unset in CI |
| `/health/deep` returned `degraded` immediately | Working as intended — PyMuPDF was genuinely absent. This endpoint is the early-warning system |

---

## 7. Glossary

- **PYQ** — Previous Year Question paper. The core input.
- **ABC analysis** — Pareto banding of topics: A ≈ first 60% of marks, B ≈ next 25%,
  C = remainder.
- **Band A topic** — high-yield; what a student studies first.
- **STR project** — the academic submission this is built for (November).
- **Viva** — oral examination where the build must be defended.
- **Agent step** — one `plan` / `act` / `observe` / `replan` phase, persisted to
  `agent_steps` with its reasoning.
- **Cut trigger** — a pre-agreed checkpoint at which a feature is dropped without debate.

---

## 8. Current state

**Done:** Steps 1–5 of the build workflow — product description, technical spec, data
model, API contracts, independent audit + revisions, EPICs, and the scaffold.

**Scaffold verified green:** ruff, mypy strict, pytest (10), eslint, tsc strict, vitest
(3), Playwright e2e (2), production build. CI runs all of it.

**Next:** EPIC 0 — database wiring, first deploy, measure free-tier reality, and collect
10–15 real question papers.

**Blocking and unresolved:**
- Hours per week (plan needs ~26; cut triggers fire below that)
- Real papers not yet collected — blocks EPIC 3, the top risk
- Kaggle dataset not yet chosen — blocks the `student_profiles` migration
