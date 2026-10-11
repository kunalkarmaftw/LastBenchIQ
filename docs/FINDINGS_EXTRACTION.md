# Findings — extraction across three subjects

> **Date:** 2026-10-11 · EPIC 0.5 complete
> Companion to `FINDINGS_CN.md`, which covers syllabus matching in depth.

Three subjects, 15 papers, **318 questions** read visually from scans. Every subject
broke a different assumption. None of these would have surfaced without real data.

| Subject | Papers | Questions | Years |
|---|---|---|---|
| Computer Networks (BCA-201/210) | 7 | 145 | 2016–2024 |
| AI (BCAT-214 + BCA-312) | 5 | 106 | 2023–2025 |
| IMED (BCA-206) | 3 | 67 | 2023–2025 |
| **Total** | **15** | **318** | |

318 questions meets the 300–500 target for the supervised classifier's training set
(`EPICS` EPIC 5) — the labelling target is reached from these three subjects alone.

---

## 1. Every page is a scan. None are digital PDFs.

21 pages examined across three files. **Zero** have a usable digital text layer.

This is not an edge case to handle — it is the only case. The tiered extraction in
`TECH_SPEC §3.4` treated vision as a fallback; on this evidence PyMuPDF text extraction
never fires at all, and vision is the only path that works.

---

## 2. The deceptive OCR layer (IMED) — the most dangerous finding

IMED pages 1–2 return ~2000 characters from `page.get_text()`. A naive check —
*"has text, therefore digital, skip OCR"* — passes, and the pipeline would proceed on
unusable data.

The text is an embedded OCR layer with **destroyed reading order**:

```
Q1 / Q2 / Note: ... / Q4 / 1) / Attempt any ten / b) / a) / b) / a) / END TERM EXAMINATION
```

Question numbers severed from their text, headers mid-page, marks floating free, plus
OCR noise (`flve`, `untt`, `Explin`, `BCa-2o6`).

**An earlier draft of this project's own analysis used exactly the failing heuristic**
(`'DIGITAL' if total_text > 500`). It would have silently produced garbage.

### Detection rule that works

```python
image_coverage = largest_image_area / page_area
is_scan = image_coverage > 0.8          # any text layer is then OCR output, distrust it
```

Verified across all 21 pages: 100% accurate. A full-page image means a scan, whatever
the text layer claims.

| Page set | Text chars | Image coverage | Correct verdict |
|---|---|---|---|
| IMED p1–2 | 1959, 1122 | 100% | scan + OCR layer — **distrust text** |
| IMED p3–5 | 0 | 95–100% | scan |
| CN, AI | 0 (mostly) | ~100% | scan |

---

## 3. Unit headers are not guaranteed (IMED)

CN and AI papers print `UNIT-I … UNIT-IV`, which made unit assignment nearly free. The
IMED 2024 and 2025 papers have **no unit headers at all** — just Q1–Q9 with an `OR`
structure.

**60% of IMED questions (40 of 67) carry no printed unit.**

Syllabus matching is therefore not an enhancement to unit assignment — for some papers
it is the *only* way to place a question. And `FINDINGS_CN.md §4` already established
that TF-IDF alone cannot do that job reliably.

---

## 4. Two courses in one file (AI)

The AI PDF mixes **BCAT-214** (4th sem, *Introduction to AI*) with **BCA-312**
(6th sem, *Artificial Intelligence*) — 43 of 106 questions from the wrong course, with a
different unit structure (BCA-312's Unit-IV is LISP and expert systems; the supplied
syllabus's Unit-IV is Learning).

Students merge PDFs without checking the paper code. The pipeline must read the paper
code from the header and warn on mismatch.

---

## 5. Orientation is baked into the image (AI)

AI page 4 is rotated 90°, but `page.rotation` reports `0`. The rotation lives in the
image pixels, not the PDF metadata, so it cannot be read from the document structure.
Orientation detection must run on the image.

---

## 6. Incomplete papers skew ranking (AI)

Two BCAT-214 papers are missing continuation pages, so their Unit-III and Unit-IV
questions are absent. Ranked as-is, those units look far less important than they are —
purely because of missing pages.

**Required:** detect an incomplete paper (unit headers present but no questions beneath;
`P.T.O.` with no following page) and either request the missing page or exclude the
paper from weighting.

---

## 7. Format drift within a single course

Even within one course code, papers are not uniform:

| Variation | Example |
|---|---|
| Max marks change | CN 75 → 60 (Dec 2024); IMED 75 → 60 (2025) |
| Q1 scheme change | `2.5×10=25`, `5×5=25`, `4×5=20`, `2×10=20` |
| Structure change | fixed questions → `Q2 OR Q3` choice |
| Course renumbered | CN: BCA-210 (sem 4) → BCA-201 (sem 3) |
| Subject renamed | IMED: "…and Entrepreneurship" → "…and Entrepreneurship Development" |

**Per-part marks cannot be assumed.** They must be read from the Q1 header
(`2.5x10=25`) or from the printed value beside each part.

---

## 8. Consolidated impact on the build

| Document | Required change |
|---|---|
| `TECH_SPEC §3.4` | Vision is the primary extraction path. Tier 1 fires only when image coverage < 80% |
| `TECH_SPEC §5.1` | `ExtractionService` gains: scan detection by image coverage, orientation detection, paper-code reading, completeness check |
| `DATA_MODEL` | `documents` needs `course_code`, `is_rotated`, `is_complete`; `questions` needs `unit_source` (`printed` vs `matched`) |
| `API_CONTRACTS` | Upload response must be able to warn: wrong course, missing pages, rotated input |
| `EPICS` EPIC 2 | Benchmark target set: 21 pages, 3 subjects, all scans |
| `EPICS` EPIC 3 | Recall denominator is **318 questions** |
| `EPICS` EPIC 5 | Labelling target met — 318 questions available now |

---

## 9. What this says about the product

Every one of these is a case a student would hit in the first week: a merged PDF with
the wrong course in it, a sideways page, a missing continuation, a scan that pretends to
have text.

A generic chatbot handed these files produces confident nonsense, because it has no way
to notice any of it. The handling above is not defensive plumbing — it is most of what
makes the product trustworthy on a real exam night.
