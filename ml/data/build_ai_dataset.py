"""Ground-truth question dataset for the AI papers, read visually from scans.

IMPORTANT: this merged PDF contains TWO DIFFERENT COURSES.

    BCAT-214  4th sem  "Introduction to Artificial Intelligence"  (2023, 2024, 2025)
    BCA-312   6th sem  "Artificial Intelligence"                  (2023, 2024)

They have different unit structures. BCA-312's Unit-IV is LISP and expert
systems; BCAT-214's Unit-IV is Learning. The 2024-25 syllabus supplied matches
BCAT-214, so BCA-312 questions are tagged `course_match=False` and must not be
mixed into the priority ranking without the student being told.

Several papers are also INCOMPLETE in the merged file (continuation pages
missing) - recorded per paper in `complete`.
"""

import json
from pathlib import Path

PAPERS: list[dict] = [
    {
        "paper_id": "AI_BCAT214_2025_MAY",
        "course_code": "BCAT-214", "course_name": "Introduction to Artificial Intelligence",
        "semester": 4, "year": 2025, "session": "May-June", "max_marks": 60,
        "course_match": True, "complete": True, "pages": [1, 2],
        "questions": [
            ("Q1", "a", "What is state space representation in problem solving?", 2, "COMPULSORY"),
            ("Q1", "b", "What are heuristic reasoning methods?", 2, "COMPULSORY"),
            ("Q1", "c", "What is the difference between predicate logic and propositional logic?", 2, "COMPULSORY"),
            ("Q1", "d", "What are a fuzzy set and a Membership function? What is the difference between a crisp set and a fuzzy set?", 2, "COMPULSORY"),
            ("Q1", "e", "Discuss the advantages of using context-free grammars in design of practical natural language parsers.", 2, "COMPULSORY"),
            ("Q1", "f", "Explain how an instance and IS-A relationship is represented in Artificial intelligence.", 2, "COMPULSORY"),
            ("Q1", "g", "Write various Knowledge Representation issues. Provide the solution of any of two issues.", 2, "COMPULSORY"),
            ("Q1", "h", "What is the purpose of discourse integration in Natural Language Processing?", 2, "COMPULSORY"),
            ("Q1", "i", "What is Conceptual Dependency?", 2, "COMPULSORY"),
            ("Q1", "j", "Define how prolog programming language is a good language for robot programming.", 2, "COMPULSORY"),
            ("Q2", "a", "Discuss the criteria for success in AI.", 6, "UNIT-I"),
            ("Q2", "b", "Discuss the history of artificial intelligence briefly", 4, "UNIT-I"),
            ("Q3", "a", "Using constraint satisfaction procedure solves the following crypt-arithmetic problem: SAVE + MORE = MONEY", 6, "UNIT-I"),
            ("Q3", "b", "Write down the steps of breadth first search. Illustrate with example.", 4, "UNIT-I"),
            ("Q4", "a", "What are the qualities of a good knowledge representation system?", 5, "UNIT-II"),
            ("Q4", "b", "Explain in detail about forward chaining and backward chaining with algorithms.", 5, "UNIT-II"),
            ("Q5", None, "Discuss the expert system in domain of medicine using suitable case study? Explain its architecture describing its components.", 10, "UNIT-II"),
            ("Q6", "a", "What is Bayesian reasoning? How does an expert system rank potentially true hypotheses? Give an example", 4, "UNIT-III"),
            ("Q6", "b", "Discuss the syntax and semantics of propositional logic. List the rules of inference for propositional logic. Consider the following facts and construct a step-by-step proof by resolution of the statement \"John likes peanuts\".", 6, "UNIT-III"),
            ("Q7", None, "What is Natural Language Processing? What are the steps in the process of Natural Language Processing? Discuss with an example.", 10, "UNIT-III"),
            ("Q8", "a", "Explain various types of learning in problem solving.", 5, "UNIT-IV"),
            ("Q8", "b", "Explain learning in Decision Tree with example", 5, "UNIT-IV"),
            ("Q9", "a", "Explain in detail about Active and Passive Reinforcement learning.", 5, "UNIT-IV"),
            ("Q9", "b", "Differentiate between Deductive and Inductive learning.", 5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "AI_BCAT214_2024_JUN",
        "course_code": "BCAT-214", "course_name": "Introduction to Artificial Intelligence",
        "semester": 4, "year": 2024, "session": "June", "max_marks": 75,
        "course_match": True, "complete": False, "pages": [3],
        "note": "Unit-IV continuation page missing from the merged PDF (Q8 partially visible, Q9 absent).",
        "questions": [
            ("Q1", "a", "What are the Various Issues in the design of the Search Problem?", 5, "COMPULSORY"),
            ("Q1", "b", "Describe Best First Search algo? Also discuss its application?", 5, "COMPULSORY"),
            ("Q1", "c", "What is difference between Generate and Test and Hill Climbing Search Techniques?", 5, "COMPULSORY"),
            ("Q1", "d", "What is AI? Mention application of AI.", 5, "COMPULSORY"),
            ("Q1", "e", "Why Knowledge representation is important in AI?", 5, "COMPULSORY"),
            ("Q1", "f", "What is Heuristic Search? Explain with suitable example", 5, "COMPULSORY"),
            ("Q1", "g", "What are State space? Write State spaces for TIC-TOE game?", 5, "COMPULSORY"),
            ("Q2", "a", "Explain the following search algorithms with example: i) A* ii) Depth First Search", 6, "UNIT-I"),
            ("Q2", "b", "How Sensors are Different from Actuators? Write PEAS for Smart Washing Machine?", 6.5, "UNIT-I"),
            ("Q3", "a", "What do you mean by agent? What are the different Types of Agents?", 6, "UNIT-I"),
            ("Q3", "b", "Discuss various problems in Hill Climbing Algorithm and how they can be prevented?", 6.5, "UNIT-I"),
            ("Q4", "a", "What are the various Issues in knowledge representations?", 6.5, "UNIT-II"),
            ("Q4", "b", "How Predicate and Propositional Logic are different from each other? Provide example", 6, "UNIT-II"),
            ("Q5", "a", "Why Knowledge Representation is important in AI? Explain with Example?", 6.5, "UNIT-II"),
            ("Q5", "b", "How Various approaches used for Knowledge representations are different from each other?", 6, "UNIT-II"),
            ("Q6", "a", "Describe one application of Natural Language Processing in detail?", 6, "UNIT-III"),
            ("Q6", "b", "What is Monotonic Reasoning and why it is important?", 6.5, "UNIT-III"),
            ("Q7", "a", "Explain the application of Fuzzy Logic? Why it is important for Automation?", 6.5, "UNIT-III"),
            ("Q7", "b", "What is the difference between Syntactic and Pragmatic processing? Explain with suitable example?", 6, "UNIT-III"),
            ("Q8", "a", "Explain different types of learnings with examples?", 6, "UNIT-IV"),
            ("Q8", "b", "Differentiate between Discovery and Analogy?", 6.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "AI_BCAT214_2023_JUL",
        "course_code": "BCAT-214", "course_name": "Introduction to Artificial Intelligence",
        "semester": 4, "year": 2023, "session": "July", "max_marks": 75,
        "course_match": True, "complete": False, "pages": [5],
        "note": "Only page 1 of 2 present. Unit-III and Unit-IV questions missing.",
        "questions": [
            ("Q1", "a", "For the given sentence \"All Pompieans were Romans\", write a well-formed formula in predicate logic.", 2.5, "COMPULSORY"),
            ("Q1", "b", "Define learning in AI.", 2.5, "COMPULSORY"),
            ("Q1", "c", "What does \"AI\" stand for, and the areas where it is applied?", 2.5, "COMPULSORY"),
            ("Q1", "d", "Illustrate constraint satisfaction.", 2.5, "COMPULSORY"),
            ("Q1", "e", "What do you mean by the term \"Agents\" in AI?", 2.5, "COMPULSORY"),
            ("Q1", "f", "Discuss Non-Monotonic Reasoning?", 2.5, "COMPULSORY"),
            ("Q1", "g", "Write a short note on Unification.", 2.5, "COMPULSORY"),
            ("Q1", "h", "What is learning by taking advice?", 2.5, "COMPULSORY"),
            ("Q1", "i", "Discuss fuzzification?", 2.5, "COMPULSORY"),
            ("Q1", "j", "Name any two applications of NLP?", 2.5, "COMPULSORY"),
            ("Q2", "a", "What is Heuristic Search? Explain with the example.", 6, "UNIT-I"),
            ("Q2", "b", "Write the steps involved in \"Hill Climbing\" algorithm? Explain the terms Local Maximum, Plateau and Ridge.", 6.5, "UNIT-I"),
            ("Q3", "a", "What is AO* algorithm? Explain with example.", 6, "UNIT-I"),
            ("Q3", "b", "Explain the concept of \"State Space Search\" and provide an illustrative example of a game that can be framed as a state space search problem. Justify your choice accordingly.", 6.5, "UNIT-I"),
            ("Q4", "a", "What is Predicate Logic? How Knowledge Representation can be achieved using it? Illustrate.", 7, "UNIT-II"),
            ("Q4", "b", "Differentiate between Forward and Backward Chaining. Explain each with example.", 5.5, "UNIT-II"),
            ("Q5", "a", "What are the various inference rules in FOL?", 6.5, "UNIT-II"),
            ("Q5", "b", "Write a program in Prolog to find the factorial of a number given by the user. Write proper comments to enhance readability of your code.", 6, "UNIT-II"),
        ],
    },
    {
        "paper_id": "AI_BCA312_2024_JUN",
        "course_code": "BCA-312", "course_name": "Artificial Intelligence",
        "semester": 6, "year": 2024, "session": "June", "max_marks": 75,
        "course_match": False, "complete": True, "pages": [4],
        "note": "DIFFERENT COURSE - 6th semester. Page is rotated 90 degrees in the source PDF.",
        "questions": [
            ("Q1", "a", "Differentiate between strong AI & weak AI?", 5, "COMPULSORY"),
            ("Q1", "b", "Differentiate between Heuristic Search & Uninformed Search.", 5, "COMPULSORY"),
            ("Q1", "c", "Define Tautology, Unsatisfiable, Satisfiable & Equivalence statements.", 5, "COMPULSORY"),
            ("Q1", "d", "Explain all connectives used in predicate logic.", 5, "COMPULSORY"),
            ("Q1", "e", "Write Converse, Inverse & Contrapositive of the conditional statement: \"Indian team wins whenever match is played in Kolkata, home town of Ganguli\".", 5, "COMPULSORY"),
            ("Q1", "f", "What is the difference between A* & AO* algorithm", 5, "COMPULSORY"),
            ("Q2", "a", "What is production system? Discuss the production rules and solution for the \"Water Jug Problem\".", 8, "UNIT-I"),
            ("Q2", "b", "Differentiate between Depth First Search and Breadth First Search", 4.5, "UNIT-I"),
            ("Q3", "a", "What is Constraint satisfaction problem? Trace the constraint satisfaction procedure to solve the following cryptarithmetic problem: SEND + MORE = MONEY", 8, "UNIT-I"),
            ("Q3", "b", "What is Turing test? Explain with diagram.", 4.5, "UNIT-I"),
            ("Q4", "a", "Explain the various issues in knowledge representation.", 8, "UNIT-II"),
            ("Q4", "b", "What is knowledge representation? Discuss various knowledge representation schemes.", 4.5, "UNIT-II"),
            ("Q5", None, "Write the following sentences in predicate logic and convert to CNF (12 given sentences).", 12.5, "UNIT-II"),
            ("Q6", "a", "What is NLP? Discuss the component of NLP.", 8, "UNIT-III"),
            ("Q6", "b", "Differentiate between context free grammar & context sensitive grammar.", 4.5, "UNIT-III"),
            ("Q7", None, "Discuss the followings: (a) Explanation based learning (b) Rote learning (c) Learning by taking advice", 12.5, "UNIT-III"),
            ("Q8", "a", "What is expert system? Write the characteristics of a good expert system.", 8, "UNIT-IV"),
            ("Q8", "b", "Explain MYCIN expert system.", 4.5, "UNIT-IV"),
            ("Q9", "a", "What is LISP? Explain the basic building blocks of with examples.", 8, "UNIT-IV"),
            ("Q9", "b", "Write a LISP program to find average of four numbers.", 4.5, "UNIT-IV"),
        ],
    },
    {
        "paper_id": "AI_BCA312_2023_JUL",
        "course_code": "BCA-312", "course_name": "Artificial Intelligence",
        "semester": 6, "year": 2023, "session": "July", "max_marks": 75,
        "course_match": False, "complete": True, "pages": [6, 7],
        "note": "DIFFERENT COURSE - 6th semester.",
        "questions": [
            ("Q1", "a", "What is Production System explain its characteristics?", 5, "COMPULSORY"),
            ("Q1", "b", "Compare Depth first Search with Best First Search by providing suitable applications?", 5, "COMPULSORY"),
            ("Q1", "c", "Describe Constraint Satisfaction Problem with Example?", 5, "COMPULSORY"),
            ("Q1", "d", "Describe Some applications of AI? With its Types?", 5, "COMPULSORY"),
            ("Q1", "e", "How AI is different from Machine Learning?", 5, "COMPULSORY"),
            ("Q1", "f", "What is the Difference between Syntactic and Semantic Processing", 5, "COMPULSORY"),
            ("Q1", "g", "What are State space? Why they are important? Show the State spaces for TIC-TOE game?", 5, "COMPULSORY"),
            ("Q2", "a", "Explain the following search algorithms with example: (i) A* (ii) Hill Climbing", 6, "UNIT-I"),
            ("Q2", "b", "What are the Various Heuristic Search Techniques? Explain with Suitable Example?", 6.5, "UNIT-I"),
            ("Q3", "a", "What are the various types of agents in AI? Write PEAS for Driverless Vehicle?", 6, "UNIT-I"),
            ("Q3", "b", "Discuss various problems in Hill Climbing Algorithm and how they can be prevented?", 6.5, "UNIT-I"),
            ("Q4", "a", "What is representing instances and is-a relationship?", 6.5, "UNIT-II"),
            ("Q4", "b", "Difference between Predicate and Propositional Logic? Provide example.", 6, "UNIT-II"),
            ("Q5", "a", "What Knowledge Representation is necessary? Explain with Example?", 6.5, "UNIT-II"),
            ("Q5", "b", "What are the Various types for Knowledge representations?", 6, "UNIT-II"),
            ("Q6", "a", "What is Natural Language Processing? and Explain its applications?", 6.5, "UNIT-III"),
            ("Q6", "b", "Write a short notes on different types of Learnings?", 6, "UNIT-III"),
            ("Q7", "a", "How learning with example is different from Rote Learning?", 6.5, "UNIT-III"),
            ("Q7", "b", "What is the difference between Discourse and pragmatic processing? Explain with suitable example?", 6, "UNIT-III"),
            ("Q8", "a", "Write a LISP for computing the Average of first five Whole Numbers?", 6, "UNIT-IV"),
            ("Q8", "b", "Differentiate between Simulation and Synthesis? And Describe any one language used for AI Modelling?", 6.5, "UNIT-IV"),
            ("Q9", "a", "Draw the Block diagram for Expert System? And Explain each Block?", 6, "UNIT-IV"),
            ("Q9", "b", "Explain any one application of Expert system in Detail?", 6.5, "UNIT-IV"),
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
                "course_name": p["course_name"], "semester": p["semester"],
                "year": p["year"], "session": p["session"],
                "paper_max_marks": p["max_marks"],
                "course_match": p["course_match"], "paper_complete": p["complete"],
                "q_no": q_no, "part": part, "text": text, "marks": marks,
                "unit_as_printed": unit,
            })
    return rows


if __name__ == "__main__":
    rows = build()
    out = Path(__file__).parent / "ai_questions_groundtruth.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    print(f"papers    : {len(PAPERS)}")
    print(f"questions : {len(rows)}")
    print()
    for p in PAPERS:
        flag = "MATCHES SYLLABUS" if p["course_match"] else "DIFFERENT COURSE"
        done = "complete" if p["complete"] else "INCOMPLETE"
        print(f"  {p['paper_id']:24s} {p['course_code']:9s} sem{p['semester']}  "
              f"{len(p['questions']):3d}q  {flag:17s} {done}")
    print()
    on = [r for r in rows if r["course_match"]]
    print(f"usable (BCAT-214)      : {len(on):3d} questions, {sum(r['marks'] for r in on):.1f} marks")
    off = [r for r in rows if not r["course_match"]]
    print(f"wrong course (BCA-312) : {len(off):3d} questions, {sum(r['marks'] for r in off):.1f} marks")
