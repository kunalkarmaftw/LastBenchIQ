"""Run the full pipeline across every subject and export one bundle for the UI.

    questions -> syllabus match -> off-syllabus gate -> marks aggregation -> ABC bands

Two-stage matching, as `FINDINGS_CN.md §4` concluded:
  1. TF-IDF cosine assigns a topic (it is good at that)
  2. a term-presence check decides off-syllabus (cosine is useless at that -
     "Modems" scored 0.071 and "ISDN" 0.069, and no threshold separates them)
"""

import json
import re
import sys
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).parent / "data"
sys.path.insert(0, str(DATA))

BAND_A_SHARE, BAND_B_SHARE = 0.60, 0.85

# Words that carry no subject meaning, so an unknown one is not evidence of
# an off-syllabus topic.
GENERIC = set("""explain discuss define describe write short note what how why the and of in a an is
are with its their various different types using give state list name mention briefly detail
example examples suitable following between difference differentiate compare comparison role
importance need significance concept about from for that this these those also any one two three
four five six seven eight nine ten can does do did has have had been being more most other others
such into over under than then them they you your our you there here when where which who whom
whose will would shall should may might must each every both few many much some such only own same
so than too very just now new old first last next good great long little well back even still way
take make made use used using work works working help helps point points part parts case cases
问题""".split())


# All-caps words that are ordinary English, not acronyms. Exam papers are full
# of them: cryptarithmetic puzzles (SEND + MORE = MONEY), emphasis, and our own
# [DIAGRAM] marker. Treating one as an unknown acronym flags a question that is
# squarely on the syllabus.
NOT_ACRONYMS = {
    "AI", "OR", "AND", "NOT", "THE", "SEND", "MORE", "MONEY", "SAVE", "DIAGRAM",
    "TIC", "TOE", "NOTE", "ALL", "ANY", "PTO", "UNIT", "BCA", "MARKS", "TIME",
}


def key_terms(text: str) -> tuple[set[str], set[str]]:
    """Acronyms and content words - the vocabulary that identifies a topic."""
    acronyms = {a for a in re.findall(r"\b[A-Z]{2,}\b", text) if a not in NOT_ACRONYMS}
    words = {w for w in re.findall(r"[a-z]+", text.lower()) if w not in GENERIC and len(w) > 3}
    return acronyms, words


def analyse(questions: list[dict], topics: list[dict]) -> dict:
    topic_docs = [t["vocabulary"] for t in topics]
    q_docs = [q["text"] for q in questions]

    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    vec.fit(topic_docs + q_docs)
    sim = cosine_similarity(vec.transform(q_docs), vec.transform(topic_docs))

    # Stage 2 vocabulary: everything the syllabus actually names.
    syllabus_words = set()
    syllabus_acronyms = set()
    for t in topics:
        a, w = key_terms(t["vocabulary"])
        syllabus_acronyms |= {x.upper() for x in a}
        syllabus_words |= w
        syllabus_words |= {x.lower() for x in a}

    matched, off = [], []
    for i, q in enumerate(questions):
        best = int(sim[i].argmax())
        acro, words = key_terms(q["text"])
        unknown_acronyms = sorted(a for a in acro if a.upper() not in syllabus_acronyms
                                  and a.lower() not in syllabus_words)
        unknown_words = sorted(w for w in words if w not in syllabus_words)

        row = {**q,
               "topic": topics[best]["topic"],
               "unit": topics[best]["unit"],
               "score": round(float(sim[i][best]), 3)}

        # ACRONYM EVIDENCE ONLY.
        #
        # An earlier version also flagged a question whose ordinary words were
        # mostly absent from the syllabus. It flagged "Draw a neat diagram of the
        # OSI model" and "Differentiate between WDM, TDM and FDM" - both squarely
        # on the syllabus - because words like "draw", "provide" and "highlighting"
        # appear in no topic description. Ordinary English is not evidence.
        #
        # An acronym the syllabus never names is strong evidence, because removed
        # topics are usually named things (ISDN, BRI, PRI, SYN, PEAS, LISP).
        # The cost is recall: a topic removed under a prose name, such as
        # "symmetric and asymmetric encryption", is not caught here. That case
        # needs the LLM adjudication stage from FINDINGS_CN section 4, which is
        # not built yet - so it is a known gap, not a silent one.
        if unknown_acronyms:
            row["reason"] = f"Not in the 2025 syllabus: {', '.join(unknown_acronyms[:3])}"
            row["unknown"] = unknown_acronyms[:3]
            off.append(row)
        else:
            matched.append(row)

    agg: dict[str, dict] = {}
    for q in matched:
        t = agg.setdefault(q["topic"], {"topic": q["topic"], "unit": q["unit"],
                                        "marks": 0.0, "count": 0, "years": set(), "qids": []})
        t["marks"] += q["marks"]
        t["count"] += 1
        t["years"].add(q["year"])
        t["qids"].append(q["question_id"])

    rows = sorted(agg.values(), key=lambda r: (-r["marks"], -r["count"]))
    total = sum(r["marks"] for r in rows) or 1.0
    cumulative = 0.0
    for r in rows:
        r["share"] = round(r["marks"] / total, 4)
        cumulative += r["share"]
        r["cumulative"] = round(cumulative, 4)
        r["band"] = "A" if cumulative <= BAND_A_SHARE else "B" if cumulative <= BAND_B_SHARE else "C"
        r["years"] = sorted(r["years"])

    return {"topics": rows, "off_syllabus": off, "matched": matched, "total_marks": total}


def main() -> None:
    from syllabus_ai_2025 import SYLLABUS as AI_SYL, flat_topics as ai_topics
    from syllabus_cn_2025 import SYLLABUS as CN_SYL, flat_topics as cn_topics
    from syllabus_imed_2025 import SYLLABUS as IM_SYL, flat_topics as im_topics
    from syllabus_nlp_2025 import SYLLABUS as NLP_SYL, flat_topics as nlp_topics

    subjects = []

    specs = [
        ("CN", "Computer Networks", CN_SYL, cn_topics, "cn_questions_groundtruth.json", None),
        ("AI", "Artificial Intelligence", AI_SYL, ai_topics, "ai_questions_groundtruth.json", "course_match"),
        ("IMED", "Management & Entrepreneurship", IM_SYL, im_topics, "imed_questions_groundtruth.json", None),
    ]

    for code, name, syl, topics_fn, qfile, filter_field in specs:
        qs = json.loads((DATA / qfile).read_text())
        excluded_course = 0
        if filter_field:
            before = len(qs)
            qs = [q for q in qs if q.get(filter_field, True)]
            excluded_course = before - len(qs)

        result = analyse(qs, topics_fn())
        papers = sorted({q["paper_id"] for q in qs})
        years = sorted({q["year"] for q in qs})
        band_a = [r for r in result["topics"] if r["band"] == "A"]

        subjects.append({
            "code": code, "name": name,
            "syllabus_code": syl.get("code", ""),
            "has_papers": True,
            "papers": len(papers), "years": [years[0], years[-1]],
            "questions": len(qs),
            "excluded_wrong_course": excluded_course,
            "units": [{"unit": u["unit"], "hours": u["hours"], "title": u["title"],
                       "topic_count": len(u["topics"])} for u in syl["units"]],
            "topics": result["topics"],
            "off_syllabus": result["off_syllabus"],
            "questions_list": [
                {"id": q["question_id"], "year": q["year"], "q": q["q_no"] + (q["part"] or ""),
                 "marks": q["marks"], "text": q["text"], "topic": q["topic"], "unit": q["unit"]}
                for q in result["matched"]
            ],
            "band_a_count": len(band_a),
            "band_a_share": round(sum(r["share"] for r in band_a), 4),
            "total_marks": result["total_marks"],
        })

    # NLP: syllabus exists, no past papers. New-subject mode.
    total_hours = sum(u["hours"] for u in NLP_SYL["units"])
    subjects.append({
        "code": "NLP", "name": "Natural Language Processing",
        "syllabus_code": "", "has_papers": False,
        "papers": 0, "years": [], "questions": 0, "excluded_wrong_course": 0,
        "units": [{"unit": u["unit"], "hours": u["hours"], "title": u["title"],
                   "topic_count": len(u["topics"]),
                   "hours_share": round(u["hours"] / total_hours, 3)} for u in NLP_SYL["units"]],
        "syllabus_topics": [{"topic": t["topic"], "unit": t["unit"]} for t in nlp_topics()],
        "topics": [], "off_syllabus": [], "questions_list": [],
        "band_a_count": 0, "band_a_share": 0, "total_marks": 0,
    })

    out = DATA / "demo_bundle.json"
    out.write_text(json.dumps({"subjects": subjects}, ensure_ascii=False))

    print(f"{'SUBJECT':<30}{'PAPERS':>7}{'QS':>6}{'TOPICS':>8}{'BAND A':>8}{'COVERS':>8}{'OFF':>5}")
    print("-" * 72)
    for s in subjects:
        if not s["has_papers"]:
            print(f"{s['name']:<30}{'-':>7}{'-':>6}{'-':>8}{'-':>8}{'-':>8}{'-':>5}  (new subject)")
            continue
        print(f"{s['name']:<30}{s['papers']:>7}{s['questions']:>6}{len(s['topics']):>8}"
              f"{s['band_a_count']:>8}{s['band_a_share']:>7.0%}{len(s['off_syllabus']):>5}")
    print(f"\nwritten: {out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
