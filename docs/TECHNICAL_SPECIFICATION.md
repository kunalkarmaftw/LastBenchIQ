# LastBenchIQ — Technical Specification

> **Status:** Draft v1 · Step 2 of the build workflow (Define the Technical Foundation)
> **Traces to:** `PRODUCT_DESCRIPTION.md`
> **Last updated:** 2026-10-11
> **Assumption:** solo developer, ~2 months, student budget. *(To confirm — if there is a team, P2 scope expands.)*

---

## 1. Purpose

This document defines *how* LastBenchIQ is built. Every decision here must serve a requirement in the Product Description. Where a decision was changed from the original plan, the reason is recorded in §3.

---

## 2. Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | **React + Vite + Tailwind CSS** | Vite is the fastest dev loop; no SSR complexity needed. Tailwind removes CSS time. |
| Charts | **Recharts** | Radar chart for skill gaps, bars for topic priority. Simple React API. |
| Backend | **Python 3.11 + FastAPI** | One language for API *and* AI/ML. Async, auto-generated Swagger docs (useful in the demo). |
| ORM | **SQLAlchemy 2.x + Alembic** | Standard Python ORM; Alembic handles schema migrations. |
| Database | **PostgreSQL** (hosted free tier: Neon or Supabase) | Relational data with clear foreign keys. Used from day one — no SQLite→Postgres migration surprises. |
| Vector store | **None in v1** — *deferred* | Nothing in P0/P1 uses RAG. See §3.6. |
| Embeddings | **None local** — *deferred* | Local `sentence-transformers` pulls in torch (~400MB+) and would exhaust the free tier's memory. If RAG is needed later, use a **hosted embedding API** so no torch is installed. |
| LLM | **Groq (Llama 3.x)** primary, provider-swappable | Free tier, very fast inference. Wrapped behind our own interface so it can be swapped. |
| Vision/OCR | **PyMuPDF** (text PDFs) → **vision LLM fallback** (scans/photos) | See §3.4 — Tesseract alone fails on phone photos. |
| Classical ML | **scikit-learn + pandas + joblib** | Trained offline, serialised to `.pkl`, loaded by the API. Industry-standard pattern. |
| Speech (interview) | **Web Speech API** (browser) | Free, low latency, no audio storage on our servers. **Note: Chrome's implementation sends audio to Google's servers** — this must be disclosed to users and stated accurately in the report (see §3.3). |
| Auth | **FastAPI + JWT** (`python-jose`, `passlib[bcrypt]`) | ~100 lines, no third-party dependency, and you learn how auth actually works. |
| File storage | **Local disk (dev) → object storage (prod)** | Behind a `StorageService` interface so the swap is one class. |
| Deployment | **Vercel** (frontend) + **Render** (API) + **Neon** (DB) | All have usable free tiers. |
| Version control | **Git + GitHub** | Required by the workflow (docs live in the repo). |

---

## 3. Challenged decisions

Per the workflow, the proposed stack was stress-tested. These five changed.

### 3.1 Dropped: Celery + Redis
**Original plan:** Celery workers with Redis for background jobs.
**Challenge:** Celery + Redis means a broker, a worker process, and a third deploy target — real ops overhead for a solo 2-month build, and a common source of "works locally, breaks in prod."
**Decision:** Use **FastAPI `BackgroundTasks`** for v1. PYQ parsing takes seconds, not minutes, and there is no job queue depth to manage at this scale.
**Revisit if:** processing a document exceeds ~30s or users complain about blocked requests.

### 3.2 Changed: build the agent loop by hand, not LangChain
**Original plan:** LangChain for agent orchestration.
**Challenge:** Three problems. (a) LangChain's abstractions hide exactly the plan–act–observe–re-plan loop you need to *demonstrate and explain* in a viva. (b) Its API churns, and tutorials go stale. (c) A debugging session inside LangChain internals costs days you don't have.
**Decision:** Write the agent loop directly against the LLM's **tool/function-calling API** — it is roughly 100–150 lines, fully inspectable, and trivially debuggable. Every step is persisted to `agent_steps` (§5.3), so the loop is *visible* rather than asserted.
**Why this is the right call for you specifically:** you can explain every line in the viva, and it matches how agents are actually built in production teams (most have moved to thin, explicit loops).
**Note:** the synopsis lists LangChain. Either update it, or keep LangChain listed only for the RAG retrieval chain, which is where it genuinely helps.

### 3.3 Changed: Web Speech API instead of Whisper (v1)
**Original plan:** OpenAI Whisper for interview speech-to-text.
**Challenge:** Whisper means audio upload, API cost per minute, and latency that hurts a live conversation. The browser already ships speech recognition.
**Decision:** **Web Speech API** for speech-to-text and browser `speechSynthesis` for text-to-speech. Free, low latency.
**Trade-offs (stated honestly):**
- Chrome-centric, and weaker on Indian-accented English.
- **Correction to an earlier draft:** this is *not* fully on-device. Chrome streams recorded audio to Google's servers for recognition. The earlier claim that "no audio leaves the browser" was wrong. Users must be told before the microphone is used, and the report must describe it accurately.
**Mitigation:** the interview always offers a **text input fallback**, so the feature never hard-depends on speech, and a student who declines the microphone can still complete an interview. Whisper stays documented as the upgrade path.

### 3.4 Changed: OCR strategy is tiered, not Tesseract-only
**Original plan:** Tesseract OCR.
**Challenge:** Students photograph question papers with phones — skewed, shadowed, sometimes handwritten. Tesseract degrades badly on exactly that input, and PYQ extraction is the P0 feature. If OCR fails, the product fails.
**Decision:** A three-tier `ExtractionService`:
1. **Digital PDF** → PyMuPDF text extraction (free, exact).
2. **Scanned/image PDF** → Tesseract with preprocessing (deskew, threshold).
3. **Low confidence or phone photo** → **vision LLM** fallback.
**Why:** the common case stays free, and the hard case still works.

### 3.6 Cut: ChromaDB, local embeddings, and RAG in v1
**Original plan:** ChromaDB + local Sentence Transformers for retrieval.
**Challenge:** Two problems. (a) **Nothing in P0 or P1 actually uses RAG** — once the
unbacked `retrieve_resources` tool was cut (§5.3), no feature needed a vector store.
(b) `sentence-transformers` installs torch, ~400MB+, on a 512MB free-tier instance that
also carries scikit-learn, pandas and PyMuPDF. It would OOM on deploy.
**Decision:** no vector store in v1. If retrieval becomes genuinely necessary, use a
**hosted embedding API** so torch is never installed locally.
**Note:** the synopsis lists ChromaDB/RAG. Either mark it future scope, or implement the
hosted-API version — do not install torch on the free tier to satisfy a document.

### 3.5 Kept, with a caveat: React
**Challenge:** A React SPA plus a separate API is more work than a single Streamlit app, and Streamlit would ship this in half the time.
**Decision:** **Keep React.** The Product Description requires real students to use it, and Streamlit's UX would not survive contact with a student on a phone at 11pm. React is also the honest "full-stack" claim for the project and your portfolio.
**Caveat:** the frontend must stay deliberately plain — Tailwind, no component library ceremony, no state-management library beyond React Query + local state.

---

## 4. Architecture

A three-tier application with a clear seam between generic AI and trained ML.

```
React (Vite + Tailwind)
        │  REST / JSON
        ▼
FastAPI  ──────────────────────────────────────────
  Auth │ Documents │ PYQ │ Career │ Interview │ ML
        │            │        │         │        │
        ▼            ▼        ▼         ▼        ▼
   PostgreSQL    Chroma   Agent Core   sklearn models (.pkl)
                              │
                    LLM provider (Groq)
```

**Three distinct intelligence layers** — this separation is the project's technical argument:

| Layer | Technology | Used for |
|---|---|---|
| **Classical ML** | scikit-learn | Prediction & ranking: placement probability, topic clustering, ATS scoring |
| **Generative AI** | LLM + RAG | Generation: revision notes, mock tests, explanations |
| **Agentic AI** | Hand-built loop + tools | Autonomous multi-step work: career planning, adaptive interviewing |

---

## 5. Services

### 5.1 Core services
| Service | Responsibility |
|---|---|
| `AuthService` | Registration, login, JWT issue/verify, password hashing |
| `StorageService` | File persistence; interface so local↔cloud is one swap |
| `ExtractionService` | Tiered document→text (§3.4), returns text + confidence |
| **`SegmentationService`** | **Raw text → `(question, marks, year, exam_type)` tuples. The project's hardest and highest-risk component — see §8.** |
| `PYQService` | Topic clustering, A/B/C banding, priority scoring |
| `NotesService` | Condensed revision notes per topic (LLM) |
| `MockTestService` | Question generation from learned patterns, scoring |
| `ResumeService` | Resume parsing, ATS scoring, skill-gap extraction |
| `MLService` | Loads `.pkl` models, exposes `predict()` with model versioning |
| `AgentCore` | The plan–act–observe–re-plan loop, tool registry, step persistence |
| `ProgressService` | Dashboard aggregates |

### 5.2 Classical ML models

| Model | Type | Algorithm | Input → Output | Serves |
|---|---|---|---|---|
| **Question Classifier** ★ | Supervised, **own labelled data** | TF-IDF + Logistic Regression (baseline) → Linear SVM / Random Forest (compare) | Question text → type (`definition`, `derivation`, `application`, `comparison`, `numerical`) | PYQ pipeline, cramming notes |
| **Placement Predictor** | Supervised, public dataset | Logistic Regression → Random Forest (compare) | Academic profile → P(placed) | Career Agent (as a tool), dashboard |
| **Topic Clusterer** | Unsupervised | TF-IDF + K-Means | Question text → topic clusters | PYQ ABC Analysis |
| **ATS Resume Scorer** | Similarity (not a trained model) | TF-IDF + cosine similarity | Resume + JD → match score | Resume Analyzer |

★ **The Question Classifier is the headline ML contribution**, because it is trained on a
dataset built by hand from real papers (`question_labels`, 300–500 rows, fixed train/test
split). It sits *inside* the P0 pipeline rather than beside it, and it supports the claim
*"I built and labelled my own dataset and evaluated a model on it"* — which a public-dataset
model alone cannot.

**Metrics — specified per model type, because one list cannot cover all four:**

| Model | Metrics reported |
|---|---|
| Question Classifier | Accuracy, precision, recall, F1 (macro + per class), **confusion matrix**, learning curve |
| Placement Predictor | Accuracy, precision, recall, F1, **confusion matrix**, ROC-AUC |
| Topic Clusterer | **Silhouette score, inertia, elbow plot** — *unsupervised: a confusion matrix does not exist for it* |
| ATS Scorer | Not a trained model. Report similarity distribution + a small manual spot-check |

> The earlier draft claimed every model would report a confusion matrix. That is false for
> K-Means and meaningless for cosine similarity. Stating the right metric per model type is
> itself a point in the viva; claiming the wrong one invites the question you cannot answer.

**Training discipline:**
- Trained in Jupyter notebooks under `/ml/notebooks/`, never in the API.
- Artefacts saved to `/ml/models/<name>.pkl` via joblib.
- Train/test split **fixed at labelling time** (`question_labels.split`) and never reshuffled.
- Always compare against a **baseline** (majority class / random) — a model that cannot beat
  "always predict the most common class" is not a result.
- `k` for K-Means justified with the **elbow method + silhouette score**, not guessed.
- Predictions logged to the `predictions` table.

### 5.3 Agent core

Both agents share one loop. Only their goal, tools, and stop condition differ.

```
plan(goal, context) → [steps]
loop (max N iterations):
    action = decide_next(state)       # LLM tool-call
    result = execute(action)          # run the tool
    state  = observe(state, result)   # update
    if goal_met(state): break
    state = replan_if_needed(state)
finalise(state) → output
```

**Hard safety rails** (a loop without these is a bill and a hang):
- `MAX_ITERATIONS = 8`
- Per-run wall-clock timeout
- Every tool call is validated against a schema before execution
- Every step row-logged to `agent_steps` — **this table is the evidence the agent is real**, and it drives a "show the reasoning trace" panel in the demo

| Agent | Tools | Stop condition |
|---|---|---|
| **Career Planning Agent** | `predict_placement` (calls the ML model), `get_skill_gaps` (reads `skill_gaps`), `web_search` (Tavily free tier) | A roadmap with ≥1 step per identified gap |
| **Adaptive Interviewer Agent** | `get_resume_context`, `evaluate_answer`, `score_interview` | Enough signal gathered, or question budget reached |

> **Three real tools, not four theatrical ones.** `query_colleges` and `retrieve_resources`
> were cut: no table backed the first, and no corpus backed the second. A tool that returns
> fabricated data makes the agent *look* agentic while proving nothing — and it is the first
> thing an examiner will probe. Every remaining tool reads something that actually exists.

> The Career Agent calling the ML model as a **tool** is the cleanest possible proof that the classical-ML and agentic layers are genuinely integrated, not bolted together.

---

## 6. Non-functional requirements

| Area | Requirement |
|---|---|
| Performance | PYQ analysis of a 20-question paper < 30s; dashboard < 1s |
| Security | Bcrypt passwords, JWT expiry, no secrets in code (`.env` + `.gitignore`), per-user data isolation on every query |
| Privacy | Resumes and papers are personal data — never logged in plaintext, deletable by the user. **Speech recognition is disclosed before the microphone is used** (§3.3): Chrome sends audio to Google. A text fallback is always offered. |
| Data isolation | Every user-owned table carries `user_id` and every query filters on it (`DATA_MODEL` preamble) |
| Cost | Must run on free tiers; local embeddings and client-side speech chosen for this reason |
| Reliability | Every LLM call wrapped with timeout + retry + graceful degradation; **the demo must never hard-fail on a network blip** |
| Testing | pytest for services; the PYQ pipeline has fixture papers with expected outputs |

---

## 7. Repository layout

```
lastbenchiq/
├── docs/            # PRODUCT_DESCRIPTION, this spec, DATA_MODEL, API_CONTRACTS
├── backend/
│   ├── app/
│   │   ├── api/         # FastAPI routers
│   │   ├── services/    # business logic (§5.1)
│   │   ├── agents/      # agent core, tools, prompts
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── core/        # config, security, db
│   ├── alembic/
│   └── tests/
├── ml/
│   ├── notebooks/   # training notebooks
│   ├── data/        # datasets (gitignored)
│   └── models/      # serialised .pkl artefacts
└── frontend/
    └── src/{pages,components,api,hooks}
```

**Rule:** business logic lives in `services/`, never in routers. Routers validate and delegate. This keeps the code testable and the viva explainable.

---

## 8. Key risks

Ranked. The top three are where this project actually dies.

| # | Risk | Impact | Mitigation |
|---|---|---|---|
| **1** | **Question segmentation fails.** Splitting raw text into questions *with marks* across arbitrary paper formats is harder than the OCR that feeds it. | No reliable questions → clustering is noise → **no product** | Collect 10–15 real papers **this week**. Build and tune the segmenter against them **before any API code**. Treat an LLM-based segmenter as the *primary* path, regex as the optimisation. |
| **2** | **Free-tier deployment discovered late.** 500MB+ deps, Tesseract needs an apt binary (not pip), Render cold starts, Groq rate limits, background tasks lost on spin-down. | Project stalls in week 7 with no time to recover | **Week 1: deploy a hello-world FastAPI + React + Neon stack with the full dependency tree installed.** Before building anything. |
| **3** | **Scope.** ~205h of plan against ~125h at 15–18 hrs/week. | Many half-built features, broken demo | Binding build order + **pre-agreed cut triggers** (`AUDIT_RESPONSE.md §6`). Cuts are decided now, not in November. |
| 4 | LLM rate limits — 10–30 students on one exam night, each generating notes | Feature fails exactly when it matters | **Cache notes per topic**, not per user. Backoff + queue. Measure the free tier's real limits in week 1. |
| 5 | Marks unparseable on phone photos | Headline "% of marks" claim invalid | `scoring_mode: frequency_only` degradation, surfaced in the API response |
| 6 | Agent loops or runs up cost | Hang / bill | Iteration cap (8), wall-clock timeout, every step logged |
| 7 | Placement dataset mismatch | Weak ML story | **Choose the dataset before migrating `student_profiles`**; derive columns from it |
| 8 | Live demo failure | Worst case on presentation day | Pre-seeded demo account (scripted, in the repo) + recorded fallback video |

---

## 9. Decisions still open

1. **Team size** — solo assumed; a teammate changes P2 feasibility.
2. **LLM provider** — Groq recommended; confirm free-tier limits are adequate before locking.
3. **Vision LLM for OCR fallback** — which provider, and is its free tier enough?
4. **Hosting** — confirm Render's free tier doesn't cold-start badly enough to hurt the demo.
