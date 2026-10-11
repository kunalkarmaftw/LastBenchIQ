# LastBenchIQ — Audit Response

> **Status:** Step 3 of the build workflow (Audit the Documentation)
> **Last updated:** 2026-10-11

An independent review of `PRODUCT_DESCRIPTION.md`, `TECHNICAL_SPECIFICATION.md`,
`DATA_MODEL.md` and `API_CONTRACTS.md` was carried out by a reviewer who did not
author them. This document records every finding and what was decided.

---

## 1. Accepted — correctness and security (non-negotiable)

| # | Finding | Fix applied |
|---|---|---|
| 1 | Placement model's inputs (`percentages`, `work_experience`) exist in no table | Added `student_profiles`, whose columns are derived **from the chosen dataset**, not invented |
| 2 | Classical ML (teacher-mandated) sat in the slippable P1 band | Promoted to **P0** |
| 3 | `user_id` missing on child tables while the stated rule forbids exceptions — IDOR risk on bare-UUID routes | `user_id` denormalised onto all user-owned child tables |
| 4 | **Factual error:** "no audio leaves the browser" — Chrome's Web Speech API streams audio to Google | Claim corrected; privacy section now states it accurately |
| 5 | "Every model reports accuracy/precision/recall/F1/confusion matrix" — impossible for K-Means (unsupervised) | Metrics now specified **per model type** |
| 6 | Cold start: K-Means on one paper (~20 questions) is noise | Hard minimum (3 papers / 50 questions) before analysis runs; empty state defined |
| 7 | `documents` had no `subject_id` though the API accepts one | Column added |
| 8 | Agent tools `query_colleges` and `retrieve_resources` had no data behind them | Cut. Agent now has **three real tools** |
| 9 | Dashboard payload returned P1/P2 data in a P0 endpoint | P0 dashboard shape defined; later fields nullable |
| 10 | `202 Accepted` convention contradicted by synchronous LLM endpoints | Convention scoped to document/analysis work only |

> Finding 4 is the one that mattered most. It was wrong, and it was the kind of
> claim an examiner could have caught in the viva.

---

## 2. Accepted — the strongest recommendation

**The classical-ML requirement was at risk of looking bolted on.**

The reviewer's argument: K-Means is unsupervised, so it yields no confusion matrix;
and a placement model trained on a public Kaggle dataset predicts nothing about
*this product's own users from its own data*. An examiner pushes exactly there.

**Adopted:** hand-label **300–500 questions** from the real papers collected, and train
a **supervised classifier on our own dataset**, sitting *inside* the P0 PYQ pipeline.

This yields a genuine train/test split, a real confusion matrix, real feature
importance — and the sentence *"I built and labelled my own dataset and evaluated a
model on it"* instead of *"I used scikit-learn."*

The Kaggle placement predictor is **kept as a second model** feeding the Career Agent,
so the ML story has both a model on own data and a model the agent calls as a tool.

---

## 3. Accepted — risk re-ranking

| Was | Now | Why |
|---|---|---|
| OCR was treated as risk #1 | **Question segmentation is risk #1** | OCR is already tiered. Turning raw text into `(question, marks, year)` across arbitrary paper formats is harder, and it had one line of spec |
| Deployment treated as a late step | **Deploy a hello-world stack in week 1** | 500MB+ dependencies, a Tesseract system binary, and cold starts on a 512MB free tier discovered in week 7 would end the project |

---

## 4. Accepted — cuts (over-engineering)

Removed because they add deploy weight or ceremony without serving a requirement:

- **ChromaDB + local Sentence Transformers** — nothing in P0 uses RAG, and torch alone
  would exhaust the 512MB free tier. *If RAG is needed later, use a hosted embedding
  API so no local torch is installed.*
- **Model registry / `GET /ml/models` / model-version plumbing** — three models trained
  once. Metrics are reported in the notebook and shown on an About page.
- **`StorageService` cloud↔local abstraction** — one production target.
- **"Provider-swappable" LLM abstraction** — a function, not an architecture.
- **`/resume/analyses/{id}/radar`** — the data already ships in the analysis response.
- **Fields:** `career_plans.status`, `roadmap_steps.due_date`, `revision_notes.model_used`,
  `subjects.code`.

**Kept deliberately:** `agent_runs`, `agent_steps`, `predictions`, and
`roadmap_steps.source_gap_id`. These are the evidence tables — they make the agentic
and ML claims inspectable rather than asserted, and that is cheap and viva-defensible.

---

## 5. Overridden — scope

The reviewer recommended cutting to the spine: PYQ pipeline, both ML models, Career
Agent, thin dashboard (~140h), and cutting the Resume Analyzer, Skill-Gap Radar and
Adaptive Interviewer.

**Decision: partially overridden.** Retained:
- **Resume Analyzer + Skill-Gap Radar** — the career chain in `PRODUCT_DESCRIPTION §4`
  depends on them; without them the positioning claim weakens.
- **Adaptive Interviewer Agent** — the strongest live-demo moment and the second half
  of the agentic story.

**Acknowledged cost:** this is approximately **205–210 hours** against a 110–125 hour
budget at 15–18 hrs/week. It is viable only at roughly **26 hrs/week**.

**Therefore scope is ordered, not merely listed.** §6 below defines checkpoints with
cut triggers agreed *in advance*, so a slip produces a pre-decided cut rather than a
broken November demo.

---

## 6. Build order and checkpoints

Work proceeds strictly in order. Nothing in a later block starts before the one
above it is working end to end.

| Block | Contents | Target |
|---|---|---|
| **0** | Hello-world deploy: FastAPI + React + Neon, full dependency tree installed | **End of week 1** |
| **1** | Auth, profile (incl. ML feature fields), upload, tiered extraction | Week 2 |
| **2** | **Question segmentation** + marks parsing, tuned on real papers | Week 3 |
| **3** | Clustering + LLM topic labelling + ABC banding + hero endpoint | Week 4 |
| **4** | Question Classifier (own labelled data) + Placement Predictor + cramming notes | Week 5 |
| **5** | Career Agent: loop, 3 tools, `agent_steps` trace panel | Week 6 |
| **6** | Resume Analyzer + Skill-Gap Radar | Week 7 |
| **7** | Adaptive Interviewer Agent | Week 7–8 |
| **8** | Hardening, seed/demo account, report, presentation | Week 8 |

### Cut triggers — decided now, not in November

- **End of week 4 — if Block 3 is not working end to end:** cut the Adaptive
  Interviewer (Block 7) immediately. No debate.
- **End of week 6 — if Block 5 is not complete:** cut the Resume Analyzer and
  Skill-Gap Radar (Block 6); the Career Agent consumes profile data directly instead.
- **Any point — Block 8 is never cut.** A working demo and a finished report outrank
  any additional feature.

> Anything cut is presented as **future scope**, deliberately and with stated reasoning.
> Scoping down with justification reads as engineering maturity. Discovering it on
> presentation day does not.

---

## 7. Still open

1. **Hours per week.** The whole plan hinges on this. At 15 hrs/week the cut triggers
   will fire; at 26 they will not.
2. **Team size** — solo assumed throughout.
3. **Collect 10–15 real question papers.** This is a blocker for Block 2, which is now
   the project's single largest risk. It should happen this week, before any code.
4. Confirm the Kaggle dataset's exact columns **before** `student_profiles` is migrated.
