"""The LastBenchIQ pipeline, run end to end on real Computer Networks papers.

    questions -> syllabus match (TF-IDF + cosine) -> marks aggregation -> ABC bands

This is the product's core claim, executed on real data:
"these N topics cover X% of marks."

The syllabus match is the step that makes it non-generic. Questions whose best
syllabus similarity falls below MATCH_THRESHOLD are reported as OFF-SYLLABUS and
excluded from the marks denominator -- a student should not spend a revision night
on a topic the university removed.
"""

import json
import sys
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, str(Path(__file__).parent / "data"))
from syllabus_cn_2025 import flat_topics  # noqa: E402

MATCH_THRESHOLD = 0.08  # tuned below; see the sensitivity table in the output
BAND_A_SHARE = 0.60
BAND_B_SHARE = 0.85


def load_questions() -> list[dict]:
    path = Path(__file__).parent / "data" / "cn_questions_groundtruth.json"
    return json.loads(path.read_text())


def match_to_syllabus(questions: list[dict], topics: list[dict], threshold: float):
    """Classical ML: TF-IDF vectors + cosine similarity, question vs topic vocabulary."""
    topic_docs = [t["vocabulary"] for t in topics]
    question_docs = [q["text"] for q in questions]

    vectoriser = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
    )
    vectoriser.fit(topic_docs + question_docs)

    sim = cosine_similarity(
        vectoriser.transform(question_docs), vectoriser.transform(topic_docs)
    )

    matched, off_syllabus = [], []
    for i, q in enumerate(questions):
        best = int(sim[i].argmax())
        score = float(sim[i][best])
        row = {**q, "match_score": round(score, 3), "matched_topic": topics[best]["topic"],
               "matched_unit": topics[best]["unit"]}
        (matched if score >= threshold else off_syllabus).append(row)
    return matched, off_syllabus


def band_topics(matched: list[dict]) -> tuple[list[dict], float]:
    """Aggregate marks per topic, then apply Pareto A/B/C banding."""
    agg: dict[str, dict] = {}
    for q in matched:
        t = agg.setdefault(
            q["matched_topic"],
            {"topic": q["matched_topic"], "unit": q["matched_unit"],
             "marks": 0.0, "count": 0, "years": set()},
        )
        t["marks"] += q["marks"]
        t["count"] += 1
        t["years"].add(q["year"])

    rows = sorted(agg.values(), key=lambda r: (-r["marks"], -r["count"]))
    total = sum(r["marks"] for r in rows)

    cumulative = 0.0
    for r in rows:
        r["share"] = r["marks"] / total
        cumulative += r["share"]
        r["cumulative"] = cumulative
        r["band"] = "A" if cumulative <= BAND_A_SHARE else "B" if cumulative <= BAND_B_SHARE else "C"
        r["years"] = sorted(r["years"])
    return rows, total


def main() -> None:
    questions = load_questions()
    topics = flat_topics()
    matched, off = match_to_syllabus(questions, topics, MATCH_THRESHOLD)
    rows, total = band_topics(matched)

    print("=" * 78)
    print("LastBenchIQ - Computer Networks (BCA-201), 7 papers 2016-2024")
    print("=" * 78)
    print(f"questions extracted : {len(questions)}")
    print(f"matched to syllabus : {len(matched)}")
    print(f"OFF-SYLLABUS        : {len(off)}  ({sum(q['marks'] for q in off):.1f} marks excluded)")
    print(f"in-syllabus marks   : {total:.1f}")

    band_a = [r for r in rows if r["band"] == "A"]
    print()
    print(f">>> {len(band_a)} topics cover {sum(r['share'] for r in band_a):.0%} of in-syllabus marks.")
    print()

    print("-" * 78)
    print(f"{'#':>2}  {'BAND':<5}{'TOPIC':<46}{'MARKS':>7}{'SHARE':>7}{'Q':>4}")
    print("-" * 78)
    for i, r in enumerate(rows, 1):
        flag = " <<<" if r["band"] == "A" else ""
        print(f"{i:>2}  {r['band']:<5}{r['topic'][:44]:<46}{r['marks']:>7.1f}{r['share']:>6.1%}{r['count']:>4}{flag}")

    print()
    print("-" * 78)
    print("OFF-SYLLABUS - appeared in past papers, NOT in the 2025 syllabus")
    print("-" * 78)
    for q in sorted(off, key=lambda x: -x["marks"]):
        print(f"  {q['year']} {q['q_no']}{q['part'] or '':<2} ({q['marks']:>4.1f}) {q['text'][:60]}")

    print()
    print("-" * 78)
    print("THRESHOLD SENSITIVITY (how many questions get excluded)")
    print("-" * 78)
    for t in (0.04, 0.06, 0.08, 0.10, 0.15, 0.20):
        m, o = match_to_syllabus(questions, topics, t)
        print(f"  threshold {t:.2f} -> matched {len(m):3d}, off-syllabus {len(o):3d}")

    out = Path(__file__).parent / "data" / "cn_analysis_result.json"
    out.write_text(json.dumps(
        {"topics": rows, "off_syllabus": off, "total_marks": total}, indent=2, default=str
    ))
    print(f"\nwritten: {out}")


if __name__ == "__main__":
    main()
