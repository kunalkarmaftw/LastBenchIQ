# Findings — Computer Networks, first real data

> **Date:** 2026-10-11 · EPIC 0.5 + a spike on EPIC 3/4
> **Data:** `ml/data/raw_papers/cn/CN_PYQ_merged.pdf` — 9 pages, **7 papers, 2016–2024**

The first time the design met real data. Three assumptions were tested; one held,
one broke, one needs redesign.

---

## 1. What the data actually is

| Paper | Code | Sem | Max | Questions |
|---|---|---|---|---|
| May–June 2016 | BCA-210 | 4 | 75 | 26 |
| May 2017 | BCA-210 | 4 | 75 | 13 |
| May 2018 | BCA-210 | 4 | 75 | 26 |
| April–May 2019 | BCA-210 | 4 | 75 | 20 |
| Jan–Feb 2023 | BCA-201 | 3 | 75 | 23 |
| January 2024 | BCA-201 | 3 | 75 | 22 |
| December 2024 | BCA-201 | 3 | **60** | 15 |

**145 questions, 880 marks offered.** Ground truth: `ml/data/cn_questions_groundtruth.json`.

**Structural observations that matter:**
- The format is highly regular: `Q1` compulsory, then `UNIT-I…IV` with two questions each,
  sub-parts `(a)`/`(b)`, marks in parentheses at the right margin. A segmenter can rely on this.
- **Marks offered exceed the paper maximum** (125 offered vs 75 max) because students attempt
  5 of 9. The denominator for ranking is *marks offered*, not paper max.
- The scheme changed in Dec 2024: 60 marks, `Q2 OR Q3` choice structure.
- The subject moved semester 4 → 3, and the code changed BCA-210 → BCA-201.
- Two papers span two pages; **papers ≠ pages**. Page 5 and page 8 are continuations.
- Some pages carry student handwriting (roll numbers, strike-throughs) and `Scanned by CamScanner`.
- Two questions embed **diagrams** that the text alone cannot convey.

---

## 2. Assumption that BROKE: Tesseract can read these papers

It cannot — specifically, **it destroys the marks column**, which is the one field the whole
ABC analysis depends on.

Observed on page 1:

| Printed | Tesseract produced |
|---|---|
| `(2.5)` | `@5)` |
| `(5)` | `©` |
| `(7.5)` | `as 7` |
| `Q1` | `QI` |
| `(a)` `(c)` `(f)` | `(@)` `(©)` `(®)` |
| `UNIT-II` | `UNIT-IT` |

Question-reference recall by page was 5/9, 4/9, 3/9 — roughly **half the questions lost**.

**Consequence:** the tiered plan in `TECH_SPEC §3.4` listed the vision model as a *fallback*.
On this evidence it is the **primary path** for scanned papers, with PyMuPDF text extraction
used only for genuinely digital PDFs. Tesseract's role shrinks to a cheap pre-check.

**Cost implication:** vision extraction is per-page and paid. Mitigation: extract **once per
paper**, persist the structured result, and never re-extract. Extraction cost is per paper, not
per student — the second student to upload the same paper costs nothing.

---

## 3. Assumption that HELD: the pipeline produces a real answer

Running `ml/analyse_cn.py` over the 145 questions:

```
questions extracted : 145
matched to syllabus : 128
off-syllabus        :  17   (87 marks excluded)

>>> 12 topics cover 60% of in-syllabus marks.
```

Top of the list, by marks across 2016–2024:

| Band | Topic | Marks | Share |
|---|---|---|---|
| A | Transport layer functions and protocols | 63.5 | 8.0% |
| A | Error detection and correction methods | 57.5 | 7.3% |
| A | Multiplexing (WDM, TDM, FDM) | 53.0 | 6.7% |
| A | Static and dynamic routing | 40.0 | 5.0% |
| A | Connection management | 38.5 | 4.9% |

This is the product's core promise, working on real papers.

---

## 4. Assumption that NEEDS REDESIGN: TF-IDF can decide syllabus membership

It cannot. The evidence is unambiguous:

| Question | In syllabus? | Cosine score |
|---|---|---|
| "Write a short note on **Modems**" | **Yes** (Unit III devices) | 0.071 |
| "Discuss **ISDN**, its services & layers" | **No** (removed) | 0.069 |

**The scores are indistinguishable.** No threshold separates them, because cosine similarity
between a 6-word question and a long topic vocabulary measures *question length*, not
membership. At the chosen threshold, 8 of 17 off-syllabus flags were wrong — including CRC,
UDP, Bridges/Routers and Modems, all of which are squarely in the syllabus.

Telling a student to skip CRC the night before a Computer Networks exam is worse than saying
nothing at all.

### What the diagnosis points to

Note what *did* work: "Modems" was assigned to **Internetworking devices** — the correct topic.
TF-IDF is adequate for **topic assignment** and useless as an **off-syllabus gate**. Those are
two different jobs and were wrongly served by one number.

A term-presence check is far sharper, because removed topics are *named entities* that appear
nowhere in the syllabus:

| Question | Unknown terms | Verdict |
|---|---|---|
| What is **SYN flooding** attack? | SYN | off-syllabus ✓ |
| What is **Broadband ISDN**? How **BRI** and **PRI** work? | ISDN, BRI, PRI | off-syllabus ✓ |
| Write a short note on **Modems** | — | in syllabus ✓ |
| In reference to **UDP** … **Pseudoheader** | — | in syllabus ✓ |
| Given a 10-bit sequence … find the **CRC** | — | in syllabus ✓ |

It still misses "symmetric and asymmetric **encryption**", where the unknown term is an ordinary
noun rather than an acronym.

### Revised design for syllabus matching

1. **TF-IDF + cosine → topic assignment** (keep; it works)
2. **Term-presence check → off-syllabus candidates** (high precision on acronyms and named entities)
3. **LLM adjudication → the ambiguous middle only** (cheap: a handful of questions per subject)
4. **Student-visible review list** — never silently drop a question; show what was excluded and why

---

## 5. The finding that justifies the feature

**ISDN appears in 4 of the 7 papers** — 2016, 2017, 2018 and 2019 — worth roughly **30 marks**,
including a full 12.5-mark question in 2017. **It is absent from the 2025 syllabus.**

A student revising from past papers would study ISDN, BRI and PRI reference points and score
nothing for it. Likewise Dec 2024's 10-mark encryption question, which belongs to no unit of
the current syllabus.

This is the argument for the whole product, in one example: a generic chatbot handed a question
paper has no idea which parts the university quietly deleted. **LastBenchIQ does, because it
holds both documents.**

---

## 6. What this changes

| Document | Change |
|---|---|
| `TECH_SPEC §3.4` | Vision extraction is the **primary** path for scans, not a fallback |
| `TECH_SPEC §5.2` | Syllabus matching is a two-stage design, not one similarity score |
| `DATA_MODEL` | `questions` needs `syllabus_topic_id`, `match_method`, `off_syllabus_reason` |
| `API_CONTRACTS §3` | Topic payload needs an `excluded_questions` block with reasons |
| `EPICS` | EPIC 3 benchmark is now concrete: **145 questions** is the recall denominator |

---

## 7. Open questions

1. **Marks for Q1 sub-parts vary by paper** (2.5 / 4 / 5). Extraction must read the header
   (`5x5=25`, `2.5x10=25`) rather than assume a per-part value.
2. **Diagram questions** — 2 of 145. Store an image crop, or mark `has_diagram` and show the
   page? Currently flagged only.
3. **Should off-syllabus questions be hidden or shown greyed-out?** Showing them, with the
   reason, is more trustworthy and lets a student overrule a wrong call.
4. **Paper-printed units drift from syllabus units.** The 2019 paper files link-state routing
   under Unit-I; the current syllabus puts routing in Unit III. Trust the syllabus match, not
   the printed header.
