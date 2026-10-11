# LastBenchIQ — EPICs

> **Status:** Draft v1 · Step 4 of the build workflow (Define the Work)
> **Traces to:** `PRODUCT_DESCRIPTION.md`, `TECHNICAL_SPECIFICATION.md`, `AUDIT_RESPONSE.md §6`
> **Last updated:** 2026-10-11

Lightweight by design. These will be revised as work proceeds — that is expected, not a
failure of planning.

---

## Standing rules

**1. Every EPIC ships its own UI.** There is no "frontend phase." An EPIC is not done when
the endpoint returns JSON; it is done when a student can do the thing in a browser on a
phone. The audit identified the frontend as the single largest undocumented effort —
folding it into each EPIC is the fix.

**2. Definition of Done — applies to every EPIC:**
- Works end to end in the **deployed** environment, not only locally
- Usable at 375px width (a student on a phone)
- Loading, empty, and error states exist — not just the happy path
- Data access is scoped by `user_id`
- No secrets in the repo
- At least one test for the core logic
- `PROJECT_STATUS.md` updated (Step 8 of the workflow)

**3. Order is binding.** No EPIC starts before the one above it works end to end.

**4. Cut triggers** (`AUDIT_RESPONSE.md §6`) are evaluated at EPIC 4 and EPIC 7.

---

## EPIC 0 — Walking Skeleton & Real Data
**Block 0 · Week 1 · ~15–20h**

**Goal:** Prove the entire stack deploys with the real dependency tree, and get real
question papers in hand — before a single feature is written.

**Why first:** The two largest risks are *deployment discovered late* and *no real papers
to build segmentation against*. Both are cheap to retire now and project-ending later.

**Stories**
- As the developer, I want a deployed hello-world across all three tiers, so that free-tier
  limits surface in week 1 instead of week 7.
- As the developer, I want 10–15 real question papers, so that segmentation is built
  against reality rather than imagination.

**Acceptance criteria**
- [ ] React (Vercel) → FastAPI (Render) → Postgres (Neon): one endpoint round-trips in production
- [ ] `requirements.txt` includes scikit-learn, pandas, PyMuPDF, pytesseract — **and the instance does not OOM**
- [ ] Tesseract system binary available in the deploy environment, with the method documented
- [ ] Measured and written down: cold-start time, memory headroom, Groq rate limits
- [ ] **10–15 real papers collected** — a deliberate mix of clean PDFs *and* phone photos, across ≥2 subjects, committed to `/ml/data/raw_papers/`
- [ ] Alembic runs a first migration against Neon
- [ ] README documents how to run and deploy

> If the dependency tree will not fit the free tier, this is when you find out — and there
> is still time to change host or trim dependencies.

---

## EPIC 1 — Identity & Student Profile
**Block 1a · Week 2 · ~10–14h**

**Goal:** A student can register, sign in, and complete the academic profile the ML model
consumes.

**Stories**
- As a student, I want to register and sign in, so my papers and plan are saved.
- As a student, I want to fill in my academic details once, so I get predictions without
  re-entering anything.

**Screens:** Register · Login · Profile form (with completion indicator)

**Acceptance criteria**
- [ ] **The Kaggle dataset is chosen first**, and `student_profiles` columns are written from its column list
- [ ] Register / login / me work; bcrypt hashing; JWT with expiry
- [ ] `is_complete` is computed, and the UI shows what is still missing
- [ ] Every protected route rejects missing or invalid tokens
- [ ] **A test proves user A cannot read user B's rows**
- [ ] Token expiry is handled in the UI (not a silent failure)

---

## EPIC 2 — Upload & Tiered Extraction
**Block 1b · Week 2 · ~25–35h**

**Goal:** A student uploads a paper in any realistic condition and gets usable text out.

**Stories**
- As a student, I want to photograph a question paper with my phone, so I don't need a scanner.
- As a student, I want to see whether extraction worked, so I know if I should retry.

**Screens:** Upload (drag/drop + camera) · Document list with status · Failure state with retry

**Acceptance criteria**
- [ ] `POST /documents` returns 202; client polls to `ready` or `failed`
- [ ] All three tiers implemented: PDF text → Tesseract (with deskew/threshold) → vision LLM
- [ ] `extraction_method` and `extraction_confidence` persisted for every document
- [ ] **Benchmarked against the real papers from EPIC 0**, with the pass rate per tier written down
- [ ] Failure produces a human-readable message and a working retry
- [ ] Stuck `processing` rows (free-tier spin-down) are requeueable
- [ ] Delete works and is scoped to the owner

> The benchmark number matters more than the code here. If tier 2 only handles 40% of phone
> photos, you need to know that now, because tier 3 then carries the product and costs money.

---

## EPIC 3 — Question Segmentation
**Block 2 · Week 3 · ~15–25h · ⚠ HIGHEST RISK**

**Goal:** Turn a wall of extracted text into discrete questions with marks, year, and type.

**Why it's the biggest risk:** This is harder than the OCR feeding it. Every downstream
feature — clustering, banding, the headline claim — is built on these tuples. If
segmentation is noisy, there is no product.

**Stories**
- As the system, I need discrete questions, so clustering has units to work with.
- As a student, I want my questions recognised even when the marks aren't printed clearly.

**Screens:** Extracted-questions review list (the student can see and correct what was found)

**Acceptance criteria**
- [ ] **LLM-based segmenter is the primary path**; regex is an optimisation, not the strategy
- [ ] Produces `(text, marks?, exam_year?, exam_type, segmentation_confidence)`
- [ ] **Benchmark:** hand-count the questions in 5 real papers; segmenter achieves **≥90% recall on question boundaries**
- [ ] Marks are parsed where present and **left null where absent — never guessed**
- [ ] Fixture tests with committed expected outputs
- [ ] The student can manually correct a mis-split question in the UI

> The manual-correction screen is not a nice-to-have. It is the escape hatch that keeps the
> product usable on the paper formats your segmenter gets wrong.

---

## EPIC 4 — Topic Clustering & ABC Analysis ★
**Block 3 · Week 4 · ~12–18h · 🚩 CHECKPOINT**

**Goal:** The product's central promise — *"these 5 topics cover 61% of marks."*

**Stories**
- As a student the night before an exam, I want to know which topics to study first, so I
  stop spreading thin time evenly across everything.
- As a new student with one paper, I want to be told what's missing, rather than shown
  meaningless results.

**Screens:** Subject view · Topic priority list with A/B/C bands · Insufficient-data state

**Acceptance criteria**
- [ ] TF-IDF + K-Means, with `k` justified by **elbow method + silhouette score**, documented in a notebook
- [ ] Clusters given human-readable names by the LLM
- [ ] ABC banding by cumulative share (A ≈ first 60%, B ≈ next 25%, C = rest)
- [ ] `insufficient_data` state below 3 papers / 50 questions — with a clear call to action
- [ ] `frequency_only` degradation when marks are unparseable, **and the wording changes from "% of marks" to "% of questions"**
- [ ] `GET /subjects/{id}/topics` returns the documented payload including `summary.message`

> 🚩 **Cut trigger:** if this EPIC is not working end to end by the end of week 4, the
> Adaptive Interviewer (EPIC 9) is cut immediately. Decided now, not in November.

---

## EPIC 5 — Classical ML Models
**Block 4a · Week 5 · ~18–27h**

**Goal:** Two trained models with honest metrics — one of them trained on a dataset you
built yourself.

**Stories**
- As a student, I want to see how likely I am to be placed, with the factors that drove it.
- As an examiner, I want to see a real confusion matrix on data the student labelled, not
  only a downloaded dataset.

**Screens:** Placement prediction card with top factors · Static "How our models work" page

**Acceptance criteria**
- [ ] **300–500 questions hand-labelled**, `split` fixed at labelling time and never reshuffled
- [ ] **Question Classifier** beats a majority-class baseline; confusion matrix + per-class F1 reported
- [ ] **Placement Predictor**: Logistic Regression vs Random Forest compared; accuracy, precision, recall, F1, ROC-AUC, confusion matrix
- [ ] Topic Clusterer reports **silhouette + inertia + elbow plot** (not a confusion matrix — it is unsupervised)
- [ ] Models serialised to `/ml/models/*.pkl`, loaded once at API startup
- [ ] `POST /ml/placement-prediction` reads `student_profiles`; refuses politely when `is_complete` is false
- [ ] `dominant_question_type` from the classifier appears in the topics payload
- [ ] Notebooks committed and re-runnable end to end

> The labelling is tedious and it is the point. "I built and labelled my own dataset and
> evaluated a model on it" is a different sentence from "I used scikit-learn."

---

## EPIC 6 — Cramming Notes
**Block 4b · Week 5 · ~6–8h**

**Goal:** Condensed, high-yield revision notes for Band A topics.

**Stories**
- As a student at 11pm, I want a one-screen summary of a topic, so I can revise it fast.

**Screens:** Topic detail with notes · Generating state

**Acceptance criteria**
- [ ] Notes generated on first request for a topic
- [ ] **Cached per topic, not per user** — 30 students revising the same topic must not cost 30 LLM calls
- [ ] Notes contain key points, formulae, and common mistakes
- [ ] Rate-limit backoff with a graceful message when the provider throttles
- [ ] Notes are readable on a phone without horizontal scrolling

---

## EPIC 7 — Career Planning Agent ★
**Block 5 · Week 6 · ~25–35h · 🚩 CHECKPOINT**

**Goal:** A genuine agent — plans, calls real tools, observes, re-plans — with its reasoning
visible on screen.

**Stories**
- As a student, I want a roadmap built around my actual profile and gaps, not a generic list.
- As an examiner, I want to see the agent's reasoning trace, not take the claim on faith.

**Screens:** Goal setup · Live "agent thinking" trace panel · Roadmap with step status

**Acceptance criteria**
- [ ] Loop implemented by hand against tool-calling — **no LangChain**
- [ ] **Three real tools**: `predict_placement` (calls the ML model), `get_skill_gaps`, `web_search`
- [ ] Hard rails: `MAX_ITERATIONS = 8`, wall-clock timeout, schema validation on every tool call
- [ ] **Every step persisted to `agent_steps`** with phase, tool, input, output, reasoning, latency
- [ ] `GET /agent-runs/{id}` returns the full trace; the UI renders it live
- [ ] Roadmap steps link back to the gap that caused them via `source_gap_id`
- [ ] Agent degrades gracefully when a tool fails — it does not hang
- [ ] **Demo check:** the trace visibly shows the agent calling the ML model as a tool

> That last criterion is the single most valuable thing in the project for the viva. It is
> the proof that the classical-ML and agentic layers are genuinely integrated rather than
> two requirements sitting side by side.
>
> 🚩 **Cut trigger:** if this EPIC is not complete by the end of week 6, EPIC 8 is cut and
> the agent reads profile data directly instead of skill gaps.

---

## EPIC 8 — Resume Analyzer & Skill-Gap Radar
**Block 6 · Week 7 · ~15–20h**

**Goal:** Turn a resume into a specific, visual gap list that feeds the roadmap.

**Stories**
- As a student, I want to see exactly which skills I'm missing for my target role.
- As the Career Agent, I need structured gaps so roadmap steps are grounded in something real.

**Screens:** Resume upload · ATS score · Skill-gap radar chart

**Acceptance criteria**
- [ ] Resume parsed into structured JSON (skills, education, projects, experience)
- [ ] **ATS score from TF-IDF + cosine** similarity against the target role
- [ ] **Per-skill levels come from the LLM, not from cosine similarity** — the similarity model produces one number, not per-skill levels, and the docs must not claim otherwise
- [ ] Gaps persisted to `skill_gaps` and consumed by the Career Agent
- [ ] Radar chart renders on mobile
- [ ] Handles a resume that parses badly, with a manual-correction path

---

## EPIC 9 — Adaptive Interviewer Agent
**Block 7 · Week 7–8 · ~25–35h · ⚠ FIRST TO BE CUT**

**Goal:** An interviewer that decides each next question from the previous answer.

**Stories**
- As a student, I want an interview that reacts to my answers, so weak areas get probed
  rather than skipped.
- As a student without a microphone, I want to type my answers and still complete it.

**Screens:** Interview session (voice + text) · Per-turn feedback · Final scorecard

**Acceptance criteria**
- [ ] Reuses the EPIC 7 agent loop — **no second implementation**
- [ ] Each answer is evaluated, and `next_action` (`probe` / `advance` / `end`) is **persisted and shown to the student**
- [ ] Questions drawn from the student's own resume context
- [ ] **Text fallback always available**; speech is never required
- [ ] **Microphone disclosure before first use** — Chrome sends audio to Google (`TECH_SPEC §3.3`)
- [ ] Question budget enforced; interview always terminates
- [ ] Scorecard written back, feeding the skill-gap picture

> **Honesty note:** a question budget with a `probe/advance/end` decision is adaptive, but
> it is closer to a well-built state machine than the Career Agent's open-ended loop. Call
> it an *adaptive interviewer* in the report, and let the Career Agent carry the "agentic"
> claim. An examiner may make this distinction before you do.

---

## EPIC 10 — Hardening, Demo & Delivery
**Block 8 · Week 8 · ~15–20h · 🔒 NEVER CUT**

**Goal:** It works on presentation day, and the report is finished.

**Stories**
- As the presenter, I want a demo that cannot fail, so a network blip doesn't cost the grade.
- As an examiner, I want a report whose claims match what was actually built.

**Acceptance criteria**
- [ ] **Seed script** creating a pre-populated demo account (papers, topics, notes, a completed agent run)
- [ ] **Recorded fallback video** of the full flow
- [ ] Every LLM call wrapped with timeout, retry, and graceful degradation
- [ ] Final docs reconciled with reality — **anything not built is listed as future scope, deliberately and with reasoning**
- [ ] Synopsis gaps reconciled: LangChain, ChromaDB/RAG, and cut features either implemented or openly restated
- [ ] Rehearsed end to end at least twice on the deployed app

> **This EPIC is never cut, never compressed.** A working demo and an honest report outrank
> any additional feature. Protect this week.

---

## Effort summary

| EPIC | Week | Est. |
|---|---|---|
| 0 Walking skeleton & data | 1 | 15–20h |
| 1 Identity & profile | 2 | 10–14h |
| 2 Upload & extraction | 2 | 25–35h |
| 3 Segmentation ⚠ | 3 | 15–25h |
| 4 Clustering & ABC ★🚩 | 4 | 12–18h |
| 5 Classical ML | 5 | 18–27h |
| 6 Cramming notes | 5 | 6–8h |
| 7 Career Agent ★🚩 | 6 | 25–35h |
| 8 Resume & gaps | 7 | 15–20h |
| 9 Interviewer ⚠ | 7–8 | 25–35h |
| 10 Hardening & delivery 🔒 | 8 | 15–20h |
| **Total** | | **181–257h** |

**Reality check:** across 8 weeks this is **23–32 hrs/week**. The cut triggers at EPIC 4 and
EPIC 7 are what make the plan survivable at the lower end of your actual availability.

**If you must cut, cut in this order:** EPIC 9 → EPIC 8 → EPIC 6.
**Never cut:** EPIC 10.
