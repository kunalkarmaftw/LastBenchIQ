# LastBenchIQ — API Contracts

> **Status:** Draft v1 · Step 2 companion
> **Traces to:** `TECHNICAL_SPECIFICATION.md`, `DATA_MODEL.md`
> **Last updated:** 2026-10-11

REST over JSON. Base path `/api/v1`. All routes except auth require
`Authorization: Bearer <jwt>`. FastAPI generates live Swagger docs at `/docs`.

**Conventions**
- IDs are UUID strings.
- Timestamps are ISO-8601 UTC.
- Errors: `{ "detail": "<message>", "code": "<machine_code>" }`
- **Document processing and subject analysis** return `202 Accepted` with a resource to poll.
- **Conversational and generation endpoints block** (note generation, interview turns). An
  LLM call of a few seconds inside a request is acceptable and far simpler than polling for
  a chat turn. The earlier blanket "never blocks" rule contradicted these endpoints; it is
  now scoped to the two cases above.

---

## 1. Auth

| Method | Path | Body → Returns |
|---|---|---|
| POST | `/auth/register` | `{email, password, name, college, branch, graduation_year}` → `{user, access_token}` |
| POST | `/auth/login` | `{email, password}` → `{user, access_token}` |
| GET | `/auth/me` | → current user |
| PATCH | `/users/me` | `{cgpa?, career_goal?, target_role?, ...}` → updated user |

---

## 2. Documents

| Method | Path | Notes |
|---|---|---|
| POST | `/documents` | multipart: `file`, `doc_type`, `subject_id?` → **202** `{document_id, status:"processing"}` |
| GET | `/documents/{id}` | → status, `extraction_method`, `extraction_confidence` |
| GET | `/documents` | `?doc_type=pyq` — list |
| DELETE | `/documents/{id}` | user can delete their own data (privacy requirement) |

> Upload returns immediately; extraction runs in a `BackgroundTask`. The client polls `GET /documents/{id}` until `status` is `ready` or `failed`.

---

## 3. PYQ analysis — P0

| Method | Path | Notes |
|---|---|---|
| POST | `/subjects` | `{name, code?}` → subject |
| GET | `/subjects` | list with document counts |
| POST | `/subjects/{id}/analyse` | **202** — runs clustering + banding over all PYQs in the subject |
| GET | `/subjects/{id}/topics` | **the core P0 response** (below) |
| GET | `/topics/{id}/questions` | questions inside a topic |
| GET | `/topics/{id}/notes` | cramming notes; generates on first request |

**`GET /subjects/{id}/topics` — the product's central payload**

```json
{
  "state": "ready",
  "subject": { "id": "...", "name": "Operating Systems" },
  "analysis": {
    "papers_analysed": 5,
    "questions_extracted": 92,
    "scoring_mode": "marks_weighted",
    "generated_at": "2026-10-11T09:00:00Z"
  },
  "topics": [
    {
      "id": "...",
      "label": "Process Scheduling",
      "priority_band": "A",
      "question_count": 14,
      "total_marks": 70,
      "share": 0.23,
      "cumulative_share": 0.23,
      "dominant_question_type": "numerical",
      "has_notes": true
    }
  ],
  "summary": {
    "band_a_topics": 5,
    "band_a_share": 0.61,
    "message": "5 topics cover 61% of marks."
  }
}
```

> `summary.message` is the moment the product proves itself. It is a first-class field, not
> something the frontend assembles. `dominant_question_type` comes from the **Question
> Classifier** — the ML model surfacing directly in the core feature.

**Two non-happy states the client must handle.** Both were missing from the first draft,
and both are the normal experience for a new user.

*Not enough data yet (a brand-new user with one paper):*
```json
{
  "state": "insufficient_data",
  "papers_analysed": 1,
  "questions_extracted": 18,
  "required": { "papers": 3, "questions": 50 },
  "message": "Upload 2 more papers to unlock topic analysis."
}
```

*Marks could not be parsed — degrade visibly, never silently:*
```json
{
  "state": "ready",
  "analysis": { "scoring_mode": "frequency_only" },
  "summary": {
    "message": "5 topics cover 61% of questions.",
    "notice": "Marks could not be read from these papers, so topics are ranked by how often they appear."
  }
}
```

> When `scoring_mode` is `frequency_only`, the wording changes from *"% of marks"* to
> *"% of questions"*. Reporting a marks percentage computed from missing marks would be
> the product lying to a student the night before an exam.

---

## 4. Practice

| Method | Path | Notes |
|---|---|---|
| POST | `/study-sprints` | `{topic_id, duration_minutes}` → sprint |
| PATCH | `/study-sprints/{id}` | `{status:"completed"}` |
| POST | `/mock-tests` | `{subject_id, question_count}` → **202** |
| GET | `/mock-tests/{id}` | test with questions |
| POST | `/mock-tests/{id}/submit` | `{answers:[{question_id, answer}]}` → score + per-question feedback |

---

## 5. Resume & skill gaps

| Method | Path | Notes |
|---|---|---|
| POST | `/resume/analyse` | `{document_id, target_role}` → **202** |
| GET | `/resume/analyses/{id}` | parsed resume, `ats_score`, skill gaps (radar plots this directly) |

```json
{
  "ats_score": 0.68,
  "skills": [
    { "skill": "Python",        "current_level": 4, "required_level": 4, "gap": 0 },
    { "skill": "System Design", "current_level": 1, "required_level": 3, "gap": 2 }
  ]
}
```

---

## 6. Career Planning Agent — agentic

| Method | Path | Notes |
|---|---|---|
| POST | `/career/plans` | `{goal, target_role?}` → **202** `{career_plan_id, agent_run_id}` |
| GET | `/career/plans/{id}` | plan + roadmap steps |
| PATCH | `/roadmap-steps/{id}` | `{status}` — student marks progress |
| **GET** | **`/agent-runs/{id}`** | **the reasoning trace** |

**`GET /agent-runs/{id}` — the agentic proof endpoint**

```json
{
  "agent_type": "career_planner",
  "goal": "Get into a top MBA programme",
  "status": "completed",
  "iterations_used": 5,
  "steps": [
    { "step_number": 1, "phase": "plan",
      "reasoning": "Need current deadlines, then feasible colleges for this CGPA." },
    { "step_number": 2, "phase": "act", "tool_name": "predict_placement",
      "tool_input": { "cgpa": 7.2 }, "tool_output": { "probability": 0.64 },
      "latency_ms": 42 },
    { "step_number": 3, "phase": "observe",
      "reasoning": "Profile is mid-tier; top-5 unrealistic. Re-planning for tier-2." }
  ]
}
```

> Exposing this over the API is deliberate: the frontend renders a live "agent thinking" panel. Step 2 above shows the **agent calling the classical ML model as a tool** — the integration of the two layers, visible in one payload.

---

## 7. Adaptive Interviewer Agent — agentic

| Method | Path | Notes |
|---|---|---|
| POST | `/interviews` | `{target_role}` → `{interview_id, first_question}` |
| POST | `/interviews/{id}/answer` | `{answer_text, answer_source}` → next question **or** end |
| GET | `/interviews/{id}` | full transcript + per-turn evaluation |
| POST | `/interviews/{id}/end` | → scorecard + feedback |

```json
{
  "turn_number": 3,
  "evaluation": { "score": 2, "max": 5, "weakness": "no concrete example" },
  "next_action": "probe",
  "next_question": "You mentioned optimising a query — what was slow, and how did you measure it?"
}
```

> `next_action` is returned to the client so the UI can show *why* the next question was chosen. Adaptivity the student can see.

---

## 8. Machine learning

| Method | Path | Notes |
|---|---|---|
| PUT | `/users/me/student-profile` | the ML feature fields (`DATA_MODEL §1`) → `{is_complete}` |
| POST | `/ml/placement-prediction` | reads `student_profiles` → probability + label |

> **Inputs come from `student_profiles`, not from arbitrary request fields.** The first
> draft accepted `percentages` and `work_experience` in the body — columns that existed in
> no table. The profile is filled once in onboarding; prediction reads it.
>
> `GET /ml/models` was cut. Three models are trained once; metrics live in the notebooks
> and on a static About page. A model registry is ceremony at this scale.

```json
{
  "probability": 0.78,
  "label": "likely_placed",
  "model_name": "placement_predictor",
  "model_version": "v2",
  "top_factors": [
    { "feature": "cgpa", "contribution": 0.31 },
    { "feature": "work_experience", "contribution": 0.18 }
  ]
}
```

> `GET /ml/models` exposes accuracy/precision/recall per model — a one-call answer when a teacher asks *"how good is your model?"*. `top_factors` keeps predictions explainable rather than a black box.

---

## 9. Dashboard

| Method | Path | Notes |
|---|---|---|
| GET | `/dashboard` | aggregated snapshot for the home screen |

**P0 shape.** Only P0 data is required; later fields are nullable and omitted until built.

```json
{
  "priority_topics": 15,
  "revision_notes": 42,
  "subjects_analysed": 3,
  "placement_probability": 0.78,
  "roadmap_progress": null,
  "last_interview_score": null,
  "next_action": {
    "type": "review_topic",
    "topic_id": "...",
    "message": "Start with Process Scheduling — Band A, 23% of marks."
  }
}
```

> The first draft returned `mock_tests_taken` and `roadmap_progress` from a P0 endpoint —
> data that belongs to features built weeks later. A P0 endpoint must be answerable from
> P0 tables.

**Empty state — a user who has uploaded nothing:**
```json
{
  "state": "empty",
  "next_action": {
    "type": "upload",
    "message": "Upload 3 past papers to see what to study first."
  }
}
```

> `next_action` is the dashboard telling the student what to do next rather than showing
> numbers and leaving them to decide. It is the connected-system promise in one field —
> and it must work on day zero, when every count is still 0.

---

## 10. Build order

Endpoints map to the build blocks in `AUDIT_RESPONSE.md §6`:

| Block | Endpoints |
|---|---|
| 0 | *(deploy hello-world — no endpoints)* |
| 1 | §1 Auth + `PUT /users/me/student-profile` → §2 Documents |
| 2 | *(segmentation — internal, no new endpoints)* |
| 3 | §3 PYQ analysis — **the hero endpoint** |
| 4 | §8 ML + `/topics/{id}/notes` |
| 5 | §6 Career Agent + `/agent-runs/{id}` |
| 6 | §5 Resume |
| 7 | §7 Interview |
| 8 | §9 Dashboard hardening, seed script |

§4 Practice (study sprints, mock tests) is **cut from v1**.
