"""Ground-truth question dataset for IMED (Introduction to Management and
Entrepreneurship Development, BCA-206), read visually from scans.

Three papers, one course - no course-mixing problem here, unlike the AI PDF.

TWO STRUCTURAL FINDINGS THIS SUBJECT INTRODUCED:

1. Pages 1-2 carry a DECEPTIVE OCR TEXT LAYER. `page.get_text()` returns ~2000
   characters, so a naive "has text -> it's digital" check passes. But the
   reading order is destroyed: question numbers are severed from their text,
   headers land mid-page, marks float free. Detection rule that works:
   a full-page image (>80% page area) means the page is a SCAN, and any text
   layer on it is OCR output to be distrusted.

2. The 2024 and 2025 papers have NO UNIT HEADERS at all - just Q1-Q9 with an
   OR structure. CN and AI both printed UNIT-I..IV, which made unit assignment
   nearly free. That cannot be assumed. Unit mapping must come from syllabus
   matching, not from paper structure.
"""

import json
from pathlib import Path

PAPERS: list[dict] = [
    {
        "paper_id": "IMED_2023_JUL",
        "course_code": "BCA-206",
        "course_name": "Introduction to Management and Entrepreneurship",
        "semester": 4, "year": 2023, "session": "July", "max_marks": 75,
        "has_unit_headers": True, "complete": True, "pages": [1, 2],
        "questions": [
            ("Q1", "a", "Differentiate between Entrepreneur and Manager.", 2.5, "COMPULSORY"),
            ("Q1", "b", "How would you define an Entrepreneurship?", 2.5, "COMPULSORY"),
            ("Q1", "c", "What are the challenges faced by an entrepreneur?", 2.5, "COMPULSORY"),
            ("Q1", "d", "Briefly describe the state of entrepreneurship in India in early years of independence.", 2.5, "COMPULSORY"),
            ("Q1", "e", "Define the role of an entrepreneur as a mentor and role model.", 2.5, "COMPULSORY"),
            ("Q1", "f", "Who is an Intrapreneur and how is it different from an entrepreneur?", 2.5, "COMPULSORY"),
            ("Q1", "g", "Specify the factors that affect the growth of economic development of a country.", 2.5, "COMPULSORY"),
            ("Q1", "h", "Can Creativity and Innovation be cultivated. Comment.", 2.5, "COMPULSORY"),
            ("Q1", "i", "What are the hindrances to innovation in entrepreneurship?", 2.5, "COMPULSORY"),
            ("Q1", "j", "Explain key principles of creative problem solving.", 2.5, "COMPULSORY"),
            ("Q1", "k", "Who in your opinion are modern entrepreneurs? Justify your answer through real world modern entrepreneur.", 2.5, "COMPULSORY"),
            ("Q2", "a", "Explain in detail various types of Entrepreneurs? Write an example of each type of Entrepreneur. Also, classify the types of Entrepreneurs specified by Clarence Danhof.", 8, "UNIT-I"),
            ("Q2", "b", "What are the general characteristics and personality traits of an entrepreneur?", 4.5, "UNIT-I"),
            ("Q3", "a", "Give description of any 5 agencies that support Entrepreneurship development in India.", 6, "UNIT-I"),
            ("Q3", "b", "Explain various types of Entrepreneurships. Also state an example of each.", 6.5, "UNIT-I"),
            ("Q4", "a", "What is creativity? Explain the process and steps of creativity.", 6, "UNIT-II"),
            ("Q4", "b", "What is SWOT analysis? Perform SWOT taking any example from the industry.", 6.5, "UNIT-II"),
            ("Q5", "a", "What is innovation? Explain the process and steps of innovation.", 6, "UNIT-II"),
            ("Q5", "b", "What is creative problem solving? Explain the techniques of creative problem solving.", 6.5, "UNIT-II"),
            ("Q6", "a", "What is out-of-box thinking? How can it be developed in an individual?", 6, "UNIT-III"),
            ("Q6", "b", "What is the role of global entrepreneurs in the development of the country? Identify any two Indian global entrepreneurs and describe their journey to success.", 6.5, "UNIT-III"),
            ("Q7", "a", "Explain the roles and responsibilities of an Entrepreneur as an Influencer. Identify any three Indian Entrepreneurs who are also the influencers.", 6, "UNIT-III"),
            ("Q7", "b", "Define Design Thinking? Explain the stages of Design Thinking and specify the examples of design thinking.", 6.5, "UNIT-III"),
            ("Q8", "a", "Explain the role and importance of Leadership in entrepreneurship. Can Leadership be developed? Justify.", 6, "UNIT-IV"),
            ("Q8", "b", "What is the difference between Leadership and Management? Identify key factors that clearly explain the difference between the two.", 6.5, "UNIT-IV"),
            ("Q9", "a", "Differentiate between entrepreneurship and business.", 5, "UNIT-IV"),
            ("Q9", "b", "Define business plan. What is its significance in entrepreneurship? Explain the process and factors important to consider while creating a business plan for your startup.", 7.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "IMED_2024_JUN",
        "course_code": "BCA-206",
        "course_name": "Introduction to Management & Entrepreneurship Development",
        "semester": 4, "year": 2024, "session": "June", "max_marks": 75,
        "has_unit_headers": False, "complete": True, "pages": [3, 4],
        "questions": [
            ("Q1", "a", "Define entrepreneurship with an example.", 5, "NONE"),
            ("Q1", "b", "State any five skills required to be an entrepreneur.", 5, "NONE"),
            ("Q1", "c", "Name the steps of creativity in entrepreneurship and elaborate.", 5, "NONE"),
            ("Q1", "d", "Briefly discuss the stages of innovation in entrepreneurship.", 5, "NONE"),
            ("Q1", "e", "State the objectives of design thinking in entrepreneurship.", 5, "NONE"),
            ("Q1", "f", "Justify the statement \"An entrepreneur can be considered a role model\".", 5, "NONE"),
            ("Q1", "g", "Define the Social Responsibility of business with an example.", 5, "NONE"),
            ("Q1", "h", "Define the main components of a comprehensive business plan.", 5, "NONE"),
            ("Q2", "a", "State any six significance of various public agencies in entrepreneurship development.", 6, "NONE"),
            ("Q2", "b", "State any seven significance of various private agencies in entrepreneurship development.", 6.5, "NONE"),
            ("Q3", "a", "State any seven roles to be played by entrepreneurs in the development of a country's economy.", 6.5, "NONE"),
            ("Q3", "b", "Enumerate any six personality traits that are significant in an entrepreneur to be successful.", 6, "NONE"),
            ("Q4", "a", "How do creativity and innovation contribute towards entrepreneurship?", 8, "NONE"),
            ("Q4", "b", "What are the day-to-day operational activities done in entrepreneurial business?", 4.5, "NONE"),
            ("Q5", "a", "Define innovation in entrepreneurship.", 2.5, "NONE"),
            ("Q5", "b", "Elaborate any ten examples of innovative decision-making toward entrepreneurial problem-solving from different sectors.", 10, "NONE"),
            ("Q6", "a", "Elaborate on the role of changing mindset and out-of-the-box thinking in entrepreneurship in present-day business.", 8, "NONE"),
            ("Q6", "b", "As a mentor, how can an entrepreneur contribute to entrepreneurship development?", 4.5, "NONE"),
            ("Q7", "a", "How the global Indian entrepreneurs have achieved success across the globe?", 6, "NONE"),
            ("Q7", "b", "'The modern entrepreneurs have achieved success in their respective sectors', justify.", 6.5, "NONE"),
            ("Q8", "a", "How is management different from leadership?", 5, "NONE"),
            ("Q8", "b", "How do the roles of entrepreneurs and managers differ within an organization?", 7.5, "NONE"),
            ("Q9", "a", "A well-developed business plan helps entrepreneurs communicate their vision and strategy to stakeholders like investors and partners, explain.", 5, "NONE"),
            ("Q9", "b", "A business plan becomes a roadmap for entrepreneurs at various stages of starting and managing a venture. Justify this statement.", 7.5, "NONE"),
        ],
    },
    {
        "paper_id": "IMED_2025_MAY",
        "course_code": "BCA-206",
        "course_name": "Introduction to Management and Entrepreneurship Development",
        "semester": 4, "year": 2025, "session": "May-June", "max_marks": 60,
        "has_unit_headers": False, "complete": True, "pages": [5],
        "questions": [
            ("Q1", "a", "Define entrepreneurship.", 5, "NONE"),
            ("Q1", "b", "Historical evolution of entrepreneurship in India.", 5, "NONE"),
            ("Q1", "c", "List the main steps involved in the creative process.", 5, "NONE"),
            ("Q1", "d", "Define innovation. How is it different from creativity?", 5, "NONE"),
            ("Q1", "e", "Define \"out-of-the-box\" thinking in the context of entrepreneurship.", 5, "NONE"),
            ("Q1", "f", "How do entrepreneurs act as role models in society?", 5, "NONE"),
            ("Q1", "g", "How does leadership influence business success?", 5, "NONE"),
            ("Q2", None, "Analyze the factors affecting entrepreneurship and explain how they impact entrepreneurial success.", 10, "NONE"),
            ("Q3", None, "Elaborate on the role of various agencies in entrepreneurship development in India. (e.g., NIESBUD, SIDBI, MSME).", 10, "NONE"),
            ("Q4", None, "Explain the necessity of creativity in entrepreneurial development. Support your answer with relevant examples.", 10, "NONE"),
            ("Q5", "a", "Describe a real-life case from any industry where an entrepreneur used creativity and innovation to solve a major problem.", 5, "NONE"),
            ("Q5", "b", "Analyze how creative thinking and decision-making go hand-in-hand in day-to-day business operations.", 5, "NONE"),
            ("Q6", None, "Evaluate the impact of entrepreneurs as mentors and influencers on budding business minds.", 10, "NONE"),
            ("Q7", None, "Compare and contrast traditional entrepreneurs with modern entrepreneurs using examples.", 10, "NONE"),
            ("Q8", None, "Discuss the importance of leadership in the success of an entrepreneurial venture.", 10, "NONE"),
            ("Q9", None, "Discuss the challenges faced by entrepreneurs in planning and managing their ventures, and suggest possible solutions.", 10, "NONE"),
        ],
    },
]


def build() -> list[dict]:
    rows = []
    for p in PAPERS:
        for q_no, part, text, marks, unit in p["questions"]:
            rows.append({
                "question_id": f"{p['paper_id']}_{q_no}{part or ''}",
                "paper_id": p["paper_id"], "course_code": p["course_code"],
                "year": p["year"], "session": p["session"],
                "paper_max_marks": p["max_marks"],
                "q_no": q_no, "part": part, "text": text, "marks": marks,
                "unit_as_printed": unit,
                "paper_has_unit_headers": p["has_unit_headers"],
            })
    return rows


if __name__ == "__main__":
    rows = build()
    out = Path(__file__).parent / "imed_questions_groundtruth.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    print(f"papers    : {len(PAPERS)}")
    print(f"questions : {len(rows)}")
    print(f"marks     : {sum(r['marks'] for r in rows):.1f}")
    print()
    for p in PAPERS:
        hdr = "unit headers" if p["has_unit_headers"] else "NO unit headers"
        print(f"  {p['paper_id']:16s} {len(p['questions']):3d}q  max {p['max_marks']}  {hdr}")
    no_unit = [r for r in rows if r["unit_as_printed"] == "NONE"]
    print()
    print(f"questions with NO printed unit: {len(no_unit)} / {len(rows)} "
          f"({len(no_unit)/len(rows):.0%}) - these need syllabus matching to place")
