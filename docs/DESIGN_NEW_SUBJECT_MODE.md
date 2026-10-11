# Design — new-subject mode (no past papers)

> **Date:** 2026-10-11
> **Trigger case:** NLP, introduced this year. Syllabus exists, zero past papers.

---

## 1. The temptation, and the measurement that killed it

NLP has no papers of its own — but the AI papers contain NLP questions. The obvious
idea: borrow that cross-subject evidence and rank NLP topics from it.

Measured against all 318 collected questions, matching them to the 27 NLP syllabus
topics:

| Unit | Topics | Topics with any evidence | Questions found |
|---|---|---|---|
| UNIT-I — Intro & preprocessing | 8 | **2** | 7 |
| UNIT-II — POS, parsing, n-grams | 5 | **1** | 1 |
| UNIT-III — Feature extraction, classification | 7 | **0** | **0** |
| UNIT-IV — Embeddings, Transformers, LLMs | 7 | **0** | **0** |

**3 of 27 topics have any evidence at all (11%). Half the syllabus has none.**

And the bias is not random. Every hit is the same shallow question — *"What is NLP?
Name its applications."* Meanwhile **Units III and IV — 14 topics, 22 teaching hours,
the entire modern half of the subject — have zero coverage.**

### What ranking on this would have produced

> *"Focus on 'Scope and applications of NLP' — it's 87% of the marks."*

A student follows that, then sits an exam on TF-IDF, Naïve Bayes, Word2Vec and
Transformers having studied none of it. **Worse than showing nothing**, because it
carries the authority of a number.

### Why the bias exists

The AI papers date from 2023–2025 but their NLP content is *classical* NLP —
syntactic/semantic/discourse processing, context-free grammars — the Rich & Knight
lineage. The new NLP syllabus is modern: embeddings, Transformers, LLMs. The subject
matter changed underneath. Borrowing across subjects imports **outdated content**, not
merely sparse content.

**Decision: cross-subject evidence is never used for ranking.** It may appear as
context on an individual topic, clearly attributed, and nothing more.

---

## 2. What new-subject mode actually does

The honest position: **without past papers there is no priority ranking.** The product
says so plainly rather than inventing one.

### Offered

1. **Syllabus structure** — units and topics, parsed from the uploaded syllabus.
2. **Teaching-hour weighting**, clearly labelled as such. The university's own hour
   allocation is the only weighting signal available: Unit I 12h (26%), II 12h (26%),
   III 12h (26%), IV 10h (22%). Flat here — which is itself the honest message:
   *nothing indicates one unit matters more.*
3. **Revision notes per topic**, generated on demand. These need no history.
4. **Practice questions**, generated from the syllabus and **labelled "generated, not
   from a past paper"** everywhere they appear.
5. **Cross-subject context, as a footnote only** — e.g. *"NLP basics appeared in 5 AI
   papers"* on the relevant topic, never folded into a score.
6. **A standing prompt to contribute**: when this year's paper exists, uploading it
   switches the subject into ranked mode.

### Explicitly not offered

- A/B/C priority bands
- Any "% of marks" figure
- Any claim about what is likely to be asked

### API shape

```json
{
  "state": "no_history",
  "subject": "Natural Language Processing",
  "message": "No past papers exist for this subject yet — it is new this year.",
  "weighting": "teaching_hours",
  "units": [
    { "unit": "UNIT-I", "hours": 12, "hours_share": 0.26, "topics": 8 }
  ],
  "available": ["revision_notes", "generated_practice"],
  "unavailable": ["priority_bands", "marks_analysis"],
  "contribute_prompt": "Upload this year's paper after your exam to unlock ranking."
}
```

This reuses the `insufficient_data` pattern already defined in `API_CONTRACTS §3`, with
a different cause and a different remedy.

---

## 3. Why this matters beyond NLP

New-subject mode is not a rare edge case:

- Syllabi are revised and subjects are added every year.
- 60% of IMED questions already have no printed unit (`FINDINGS_EXTRACTION §3`), so
  syllabus-only handling is already load-bearing.
- A brand-new user with one uploaded paper hits a near-identical empty state.

It also carries the product's central promise. A generic chatbot asked *"what should I
study for NLP?"* answers confidently from training data that knows nothing of this
syllabus. **LastBenchIQ's better answer is the more modest one** — here is your actual
syllabus, here is what the hours suggest, and here is the honest admission that nobody
can know what will be asked in a subject's first year.

Saying "I don't know, and here is why" is the trustworthy move, and it is the thing a
chatbot will not do.

---

## 4. Changes required

| Document | Change |
|---|---|
| `PRODUCT_DESCRIPTION §6` | New-subject mode is part of P0, not a later nicety |
| `API_CONTRACTS §3` | Add the `no_history` state above |
| `DATA_MODEL` | `subjects` needs `has_past_papers`; `topics` needs `source` (`pyq_derived` vs `syllabus_derived`) and nullable priority fields |
| `EPICS` EPIC 4 | Acceptance criteria must cover a subject with zero papers |
| `CLAUDE.md` | Degradation table gains: *no past papers → state the limit, never invent a ranking* |
