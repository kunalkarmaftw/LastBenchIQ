# LastBenchIQ — Data Model

> **Status:** Draft v1 · Step 2 companion
> **Traces to:** `TECHNICAL_SPECIFICATION.md`
> **Last updated:** 2026-10-11

PostgreSQL via SQLAlchemy. All IDs are UUIDs. All tables carry `created_at`.

**Every user-owned table carries a `user_id` column and is filtered by it on every
query — no exceptions.** Child tables denormalise `user_id` rather than relying on a
join to their parent. This costs one column and removes an entire class of
broken-access-control bug: routes take bare UUIDs (`PATCH /roadmap-steps/{id}`), so
without it, any handler that forgets to join through to `users` leaks another
student's data.

---

## 1. Identity

### `users`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| email | varchar unique | login |
| password_hash | varchar | bcrypt |
| name | varchar | |
| college | varchar | |
| branch | varchar | e.g. BCA, CSE |
| graduation_year | int | |
| cgpa | numeric(3,2) | feeds the placement model |
| career_goal | enum | `mba` \| `job` \| `undecided` |
| target_role | varchar | e.g. "Backend Developer" |

> `cgpa`, `branch`, and `target_role` are not profile decoration — they are **model inputs** and **agent context**.

### `student_profiles`
The features the Placement Predictor actually consumes. Kept separate from `users`
because these columns are **derived from the training dataset, not invented**.

> **Build rule:** choose the Kaggle dataset *first*, read its column list, and write
> this table to match. Writing the schema before picking the dataset is what produced
> the original mismatch — the API asked for `percentages` and `work_experience` that
> existed nowhere.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users, unique | one profile per user |
| ssc_percentage | numeric | class 10 |
| hsc_percentage | numeric | class 12 |
| degree_percentage | numeric | |
| degree_stream | varchar | |
| work_experience | boolean | |
| entrance_test_percentage | numeric | nullable |
| specialisation | varchar | nullable |
| is_complete | boolean | false until every model input is filled |

> `is_complete` matters: the Career Agent must not call `predict_placement` on a
> half-filled profile. When false, the agent asks the student to complete it instead
> of predicting from nulls.

---

## 2. Documents & extraction

### `documents`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | |
| subject_id | UUID FK → subjects | nullable; required for `pyq` |
| doc_type | enum | `pyq` \| `syllabus` \| `resume` |
| original_filename | varchar | |
| storage_path | varchar | |
| status | enum | `uploaded` \| `processing` \| `ready` \| `failed` |
| retry_count | int | background tasks are lost when a free-tier instance spins down; a stuck `processing` row must be requeueable |
| extraction_method | enum | `pdf_text` \| `ocr` \| `vision_llm` |
| extraction_confidence | float | drives the tier fallback |
| extracted_text | text | |
| error_message | text | nullable |

> `extraction_method` + `extraction_confidence` exist so OCR quality is **measurable**, not guessed. You will need this when debugging real phone photos.

### `subjects`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK | |
| name | varchar | e.g. "Operating Systems" |
| code | varchar | nullable |

---

## 3. PYQ analysis (P0)

### `questions`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | denormalised (see preamble) |
| document_id | UUID FK → documents | |
| subject_id | UUID FK → subjects | |
| text | text | the question |
| marks | int | **nullable — frequently unparseable** |
| exam_year | int | nullable |
| exam_type | enum | `midterm` \| `endterm` \| `unknown` |
| topic_id | UUID FK → topics | nullable until clustered |
| segmentation_confidence | float | how reliably this was split out of raw text |

> **Marks are the weak link.** On phone photos, marks sit in margins and are often
> lost. Everything downstream — banding, the "covers 61% of marks" headline — is marks
> arithmetic. The fallback is defined in `topics` below, not left to chance.

### `question_labels`
The hand-labelled training set for the supervised classifier — the model trained on
**our own data**, which is what makes the classical-ML requirement genuine rather than
borrowed from a public dataset.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| question_id | UUID FK → questions | |
| label | varchar | e.g. `definition` \| `derivation` \| `application` \| `comparison` \| `numerical` |
| bloom_level | varchar | nullable: remember / understand / apply / analyse |
| labelled_by | varchar | provenance |
| split | enum | `train` \| `test` — fixed at labelling time, never reshuffled |

> Target: **300–500 labelled questions.** Fixing `split` at labelling time prevents
> accidentally re-splitting between runs and reporting inflated accuracy — the kind of
> mistake an examiner looks for.

### `topics`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | denormalised |
| subject_id | UUID FK | |
| label | varchar | human-readable cluster name (LLM-named) |
| cluster_id | int | raw K-Means cluster index |
| question_count | int | frequency |
| total_marks | int | weightage; 0 when marks were unparseable |
| priority_score | float | computed ranking score |
| priority_band | enum | `A` \| `B` \| `C` |
| scoring_mode | enum | `marks_weighted` \| `frequency_only` |

**Banding rule (documented, not arbitrary):** topics are sorted by `priority_score`, then
cumulative coverage decides the band — **A** = topics covering the first ~60%, **B** = next
~25%, **C** = remainder. This is a true *ABC analysis* (Pareto) and is defensible in the viva.

**Degradation rule:** when marks cannot be parsed for a subject, `scoring_mode` becomes
`frequency_only`, `priority_score` falls back to question frequency alone, and **the API
response says so explicitly**. The feature degrades visibly instead of silently reporting
a marks percentage computed from missing data.

**Minimum data rule:** analysis requires **≥3 papers and ≥50 questions**. Below that,
K-Means on short strings produces noise and silhouette scores are meaningless. The API
returns an explicit `insufficient_data` state, not bad clusters.

### `revision_notes`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | denormalised |
| topic_id | UUID FK → topics | |
| content | text | LLM-generated condensed note |

---

## 4. Practice

### `study_sprints`
| id, user_id, topic_id, duration_minutes, started_at, completed_at, status |

### `mock_tests`
| id, user_id, subject_id, generated_at, total_marks, score (nullable) |

### `mock_test_questions`
| id, mock_test_id, question_text, expected_answer, marks, student_answer, awarded_marks |

---

## 5. Career track

### `resume_analyses`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id, document_id | UUID FK | |
| target_role | varchar | |
| parsed_json | jsonb | skills, education, projects, experience |
| ats_score | float | from the TF-IDF + cosine model |

### `skill_gaps`
| id, **user_id**, resume_analysis_id, skill, required_level, current_level, gap_score |

> `required_level` / `current_level` (1–5) cannot come from TF-IDF cosine similarity —
> that yields one similarity number, not per-skill levels. **Source:** the LLM extracts
> per-skill levels during resume parsing; the TF-IDF cosine model produces only the
> overall `ats_score`. Keeping these separate avoids claiming the classical model does
> something it cannot.

> `skill_gaps` is what the radar chart plots **and** what the Career Agent reads to decide roadmap steps. One table, two consumers — this is the "chain" from the Product Description made concrete.

### `career_plans`
| id, user_id, goal, created_at |

### `roadmap_steps`
| id, **user_id**, career_plan_id, step_order, title, description, resource_url, status (`todo` \| `doing` \| `done`), source_gap_id (FK → skill_gaps, nullable) |

> `source_gap_id` links each roadmap step back to the gap that caused it — so the plan is **explainable**, not a generic list.

---

## 6. Agentic AI (the evidence tables)

### `agent_runs`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK | |
| agent_type | enum | `career_planner` \| `interviewer` |
| goal | text | the goal given to the agent |
| status | enum | `running` \| `completed` \| `failed` \| `max_iterations` |
| iterations_used | int | |
| started_at / finished_at | timestamp | |

### `agent_steps`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | denormalised |
| agent_run_id | UUID FK | |
| step_number | int | |
| phase | enum | `plan` \| `act` \| `observe` \| `replan` |
| tool_name | varchar | nullable (null on plan/observe) |
| tool_input | jsonb | |
| tool_output | jsonb | |
| reasoning | text | the model's stated reasoning |
| latency_ms | int | |

> **These two tables are the most important in the project.** They turn "it's agentic" from a claim into a queryable reasoning trace you can render on screen during the presentation. If an evaluator asks *"where is the agent loop?"*, you show this table.

---

## 7. Interview

### `interviews`
| id, user_id, target_role, started_at, ended_at, overall_score, feedback_summary, agent_run_id (FK) |

### `interview_turns`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | denormalised |
| interview_id | UUID FK | |
| turn_number | int | |
| question | text | |
| answer_text | text | from speech or typed |
| answer_source | enum | `speech` \| `text` |
| evaluation | jsonb | score + reasoning per turn |
| next_action | enum | `probe` \| `advance` \| `end` |

> `next_action` records the **decision** the agent made after each answer. That column is the difference between an adaptive interviewer and a fixed question list.

---

## 8. Machine learning

### `predictions`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK | |
| model_name | varchar | e.g. `placement_predictor` |
| model_version | varchar | e.g. `v2` |
| input_features | jsonb | exact features used |
| output_value | float | probability |
| output_label | varchar | e.g. `likely_placed` |

> Logging `model_version` + `input_features` is standard MLOps practice: it means a prediction can be reproduced and explained months later.

---

## 9. Relationship summary

```
users ──┬── student_profiles                    (ML features → Placement Predictor)
        │
        ├── subjects ──────┬── documents ──── questions ──┬── question_labels
        │                  │                      │        └── (supervised classifier)
        │                  └── topics ◄────────────┘
        │                        ├── revision_notes
        │                        └── study_sprints
        │
        ├── resume_analyses ──── skill_gaps
        │                             │  source_gap_id
        ├── career_plans ──── roadmap_steps ◄┘
        ├── agent_runs ────── agent_steps
        ├── interviews ────── interview_turns
        ├── mock_tests ────── mock_test_questions
        └── predictions
```

**The two chains, visible in the schema:**
- **Exam:** `documents → questions → topics → revision_notes → study_sprints`
- **Career:** `resume_analyses → skill_gaps → roadmap_steps` (via `source_gap_id`)

Both chains hand data forward without the student re-entering anything. That is the
Product Description's central claim, expressed as foreign keys.
