# LastBenchIQ — Product Description

> **Status:** Draft v1 · Step 1 of the build workflow (Define the Goal)
> **Owner:** Kunal Verma (Karma)
> **Last updated:** 2026-10-11

This document is the source of truth for *what* LastBenchIQ is and *who* it serves.
It is deliberately non-technical. No stack, no architecture, no implementation.
Every later document (technical spec, EPICs, prompts) must trace back to this one.

---

## 1. One-line description

**LastBenchIQ is a connected AI companion for final-year college students that turns their own question papers, syllabus, and resume into one adaptive plan — covering both exams and what comes after graduation.**

---

## 2. The problem

Final-year students are under pressure on two fronts at the same time, and the support for both is fragmented and generic.

**On exams:**
- Students prepare the night before with no idea which topics actually carry marks.
- Time is the scarcest resource, and it gets spent on low-yield material.
- Revision means re-reading everything, because nothing tells them what to prioritise.

**On what comes next:**
- Choosing between higher studies (MBA) and a job is made from scattered senior advice, random blogs, and guesswork.
- Students don't know where to apply, when to apply, or what is realistic for their profile.
- They get generic skill advice and never see a concrete, role-specific picture of what they're missing.
- Real practice — mock interviews, viva, quality practice papers — is expensive or simply unavailable.

**The deeper problem:** Students already have AI tools, but every tool is a dead end. Each answer is one-shot and disconnected. Nothing remembers them, nothing carries one result into the next decision, and nothing follows them across the whole year.

---

## 3. Target user

### Primary (v1)
**Final-year undergraduate students in India**, who are simultaneously:
- preparing for mid-term and end-term exams, and
- deciding between higher studies (MBA/masters) and placement.

This is the sharpest user because both halves of the product matter to them *at the same time*. They feel the full problem.

### Secondary (later)
Junior-year students (1st–3rd year), who need the exam half now and the career half later.
**Not a v1 target.** The product widens to them only after v1 works.

---

## 4. Positioning — why this, not ChatGPT

The honest answer is **not** "it has more features." A student can paste a question paper into any chatbot.

**LastBenchIQ's claim is that the pieces are connected and it remembers you.**

| A generic chatbot | LastBenchIQ |
|---|---|
| Every session starts from zero | Knows your syllabus, papers, resume, and progress |
| Each answer is a dead end | Each result feeds the next step |
| You re-explain yourself every time | It tracks you across the whole final year |
| Gives information | Runs a plan and adapts it |

**The two chains that prove the claim:**

1. **Exam chain:** upload PYQs → topics ranked by weightage → condensed notes for the top topics → timed study sprint on those notes → mock test generated from the same patterns.
2. **Career chain:** state your goal → resume parsed → skill gaps identified → roadmap built around those gaps → mock interview drawn from your own resume → results fed back into the skill-gap picture.

No step in either chain is re-typed by the student. That hand-off between steps is the product.

**Positioning statement:**
> Not another AI tool. One connected system that knows your papers, your profile, and your progress — and keeps adapting both your study plan and your career plan from the same memory.

---

## 5. What success looks like

Two definitions of success, both required.

### A. Academic (primary, November deadline)
- The STR project is submitted and presented successfully.
- The project demonstrates genuine technical depth: **classical ML**, **agentic AI**, and a working full-stack application — not an LLM wrapper.
- The live demo works end to end without failing.

### B. Real usage (the harder, more meaningful goal)
- Real students at the college use LastBenchIQ to prepare for an actual exam cycle.
- At minimum: a student uploads their own PYQs and reports the priority list changed what they studied.
- Target: a small number of real users (10–30) during one end-term cycle, not a hypothetical user base.

**Why both matter:** the academic goal sets the deadline; the real-usage goal keeps the product honest. A feature that demos well but no student would actually open is a failed feature.

---

## 6. Scope

### The one feature that must exist
**PYQ ABC Analysis.** If nothing else ships, this ships. It is the most universally useful part, it serves every student regardless of career track, and it is the entry point that brings students in.

> Revised after the Step 3 audit. Build order and cut triggers: `AUDIT_RESPONSE.md §6`.

### P0 — Must ship by November
| Feature | What it does for the student |
|---|---|
| Account & profile | Goal (MBA/job), CGPA, and the academic fields the ML model needs |
| Upload & ingestion | PYQs, syllabus, resume as PDF/image, with tiered extraction |
| **Question segmentation** | Raw text → individual questions with marks. *The hardest piece; everything depends on it.* |
| **PYQ ABC Analysis** | Ranks topics into A/B/C bands by frequency and weightage |
| **Question Classifier** (classical ML) | Supervised model trained on **our own hand-labelled data**, inside the pipeline |
| **Placement Predictor** (classical ML) | Trained classifier the Career Agent calls as a tool |
| Cramming Notes | Condensed revision notes for high-priority topics |
| Student dashboard | One place to see the plan and act on it |

> **Why both ML models are P0:** classical ML is a pass/fail academic requirement. Anything
> in a lower band can slip, and the one non-negotiable requirement must not be the thing
> that slips.

### P1 — The agentic claim
| Feature | Why it matters |
|---|---|
| **Career Planning Agent** (agentic) | Plans, calls 3 real tools, observes, re-plans — with a visible reasoning trace |
| Resume Analyzer + Skill-Gap Radar | Completes the career chain: resume → gaps → roadmap steps |

### P2 — Committed, but first to be cut if behind
| Feature | Why it matters |
|---|---|
| **Adaptive Interviewer Agent** (agentic) | The strongest live-demo moment; reuses the Career Agent's loop |

### Cut from v1 — presented as future scope
Mock Test Generation · Study Sprint Mode · LinkedIn content suggestions · AI Viva
Simulator · RAG / vector store

> These were cut to protect the quality of what ships. Each is named in the report as
> deliberate future scope with stated reasoning.

### Explicitly out of scope (v1)
These are **not** being built, and saying so protects the timeline:
- Live scraping of institutional or university databases
- A social network, peer matching, or senior-mentorship marketplace
- Multi-agent group discussion or panel interview simulation *(pitched as future scope only)*
- Payments, subscriptions, or any monetisation
- Mobile native apps (responsive web only)
- Languages other than English for v1
- Any guarantee of exam results or placement outcomes

---

## 7. Non-goals and honest limits

Stating these prevents over-promising in the report and the demo:

- **It does not guarantee outcomes.** It surfaces priorities and guidance, not guaranteed marks or jobs.
- **It is not a replacement for teaching.** It prioritises and practises; it does not replace the syllabus or a teacher.
- **Predictions are probabilistic.** The placement predictor outputs a likelihood from historical data, and must always be presented as such.
- **PYQ quality depends on what students upload.** The system is only as good as the papers it is given.
- **It is not a content library.** It does not host or sell notes; it generates from the student's own material.

---

## 8. Constraints

| Constraint | Value |
|---|---|
| Hard deadline | November 2026 (STR presentation) |
| Build time | ~8 weeks |
| **Hours per week** | **Open — the plan requires ~26 hrs/week.** At 15–18 the cut triggers in `AUDIT_RESPONSE.md §6` will fire. |
| Team | *(to confirm — solo assumed)* |
| Budget | Student budget — free tiers and open-source wherever possible |
| Required by mentor | Must include **classical ML**, not only LLM calls |

---

## 9. Guiding principles

Decisions throughout the build defer to these, in order:

1. **The chain over the feature.** A feature that doesn't hand its output to another feature is suspect. The connection is the product.
2. **A student must actually open it.** If a feature only impresses evaluators and no student would use it on a real exam night, cut it.
3. **Depth over count.** Two features that genuinely work beat seven half-built ones. The demo must never break.
4. **Honest labels.** "Agentic" only describes features with a real plan–act–observe–re-plan loop. "AI-powered" for everything else. No inflated claims.
5. **Ship the spine first.** PYQ analysis and the dashboard before anything clever.

---

## 10. Open questions

- Team composition: solo or with teammates? (drives how much of P2 is realistic)
- Which college/exam pattern is v1 validated against?
- Can real PYQs be collected before the build starts, so there is real test data from day one?
