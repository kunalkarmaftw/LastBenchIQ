# LastBenchIQ — Project Status

> Updated after every EPIC (Step 8 of the workflow: maintain the feedback loop).
> Future sessions read this first to know where things stand.

**Last updated:** 2026-10-11 (EPIC 0.1 complete)

---

## Where we are

**Planning complete.** Steps 1–6 of the build workflow are done. No feature code written yet.

| Step | Output | State |
|---|---|---|
| 1 Define the goal | `PRODUCT_DESCRIPTION.md` | ✅ |
| 2 Technical foundation | `TECHNICAL_SPECIFICATION.md`, `DATA_MODEL.md`, `API_CONTRACTS.md` | ✅ |
| 3 Audit the docs | `AUDIT_RESPONSE.md` — independent review, 10 fixes applied | ✅ |
| 4 Define the work | `EPICS.md` — 11 EPICs, 72 acceptance criteria | ✅ |
| 5 Scaffold | CI, strict linting, 4 test layers — **verified green** | ✅ |
| 6 Final preparation | `CLAUDE.md`, `KNOWLEDGE_BASE.md`, `PROMPT_TEMPLATE.md` | ✅ |
| 7 Execute EPICs | — | ⬜ next |

---

## EPIC progress

| EPIC | Week | State |
|---|---|---|
| 0 Walking skeleton & real data | 1 | 🟡 code complete — **0.1 database done**, 0.2–0.4 configs + script ready, awaiting your hosting accounts. 0.5 papers **done** (318 questions) |
| 1 Identity & profile | 2 | ⬜ |
| 2 Upload & extraction | 2 | ⬜ |
| 3 Segmentation ⚠ | 3 | ⬜ |
| 4 Clustering & ABC ★🚩 | 4 | ⬜ |
| 5 Classical ML | 5 | ⬜ |
| 6 Cramming notes | 5 | ⬜ |
| 7 Career Agent ★🚩 | 6 | ⬜ |
| 8 Resume & gaps | 7 | ⬜ |
| 9 Interviewer ⚠ | 7–8 | ⬜ |
| 10 Hardening & delivery 🔒 | 8 | ⬜ |

🚩 cut-trigger checkpoint · ⚠ first to be cut · 🔒 never cut

---

## What the scaffold already delivered

- Repo, CI pipeline (backend / frontend / e2e / secret-scan jobs)
- ruff + mypy strict; eslint + tsc strict
- Tests at four levels: unit, API, component, e2e — all passing
- `UserOwnedMixin` making the `user_id` rule structural
- `/health/deep` reporting heavy dependencies and the Tesseract binary
- Dockerfile installing and verifying Tesseract at build time

---

## Blocking items

| # | Item | Blocks | Why it matters |
|---|---|---|---|
| 1 | **Collect 10–15 real question papers** | EPIC 2, 3 | Risk #1 (segmentation) cannot be built or benchmarked without them |
| 2 | **Choose the Kaggle placement dataset** | EPIC 1, 5 | `student_profiles` columns must be derived from it, not invented |
| 3 | **Confirm hours per week** | the whole plan | Needs ~26h/wk; below that, cut triggers fire |
| 4 | Confirm solo vs team | scope | Solo assumed throughout |

---

## Next action

Run **EPIC 0.1** (`PROMPT_TEMPLATE.md`) — wire the database and the first migration —
and in parallel, collect the papers (EPIC 0.5). The papers are not code and are the
higher-leverage of the two.

---

## Decision log

| Date | Decision | Where |
|---|---|---|
| 2026-10-11 | Dropped Celery/Redis, LangChain, Whisper, Tesseract-only OCR | `TECH_SPEC §3` |
| 2026-10-11 | Both ML models promoted to P0 (academic requirement cannot slip) | `AUDIT_RESPONSE §1` |
| 2026-10-11 | Hand-labelled question classifier adopted as the headline ML story | `AUDIT_RESPONSE §2` |
| 2026-10-11 | Vector store / RAG cut from v1 (torch would OOM the free tier) | `TECH_SPEC §3.6` |
| 2026-10-11 | Resume Analyzer + Interviewer kept against audit advice; cut triggers added instead | `AUDIT_RESPONSE §5` |
