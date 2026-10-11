"""Introduction to Artificial Intelligence syllabus (BCAT-214, 2024-25 onwards)."""

SYLLABUS = {
    "subject": "Artificial Intelligence",
    "code": "BCAT-214",
    "year": 2025,
    "units": [
        {
            "unit": "UNIT-I", "hours": 12,
            "title": "Overview of AI, Problem Space and Heuristic Search",
            "topics": [
                ("Introduction and importance of AI", ["introduction to AI", "importance of AI", "what is AI", "applications of AI", "AI and its related field", "AI techniques", "strong AI weak AI", "history of artificial intelligence"]),
                ("Criteria for success in AI", ["criteria for success", "Turing test"]),
                ("State space search", ["state space", "state space representation", "defining the problem as a state space search", "state spaces for TIC-TOE"]),
                ("Production systems", ["production system", "production rules", "water jug problem", "characteristics of production system"]),
                ("Issues in design of search programs", ["issues in the design of the search programs", "issues in design of search"]),
                ("Generate and test", ["generate and test"]),
                ("Hill climbing", ["hill climbing", "local maximum", "plateau", "ridge"]),
                ("Best first search", ["best first search", "A* algorithm", "AO* algorithm", "heuristic search", "heuristic reasoning"]),
                ("Problem reduction", ["problem reduction"]),
                ("Constraint satisfaction", ["constraint satisfaction", "cryptarithmetic", "crypt-arithmetic", "SEND MORE MONEY"]),
            ],
        },
        {
            "unit": "UNIT-II", "hours": 12,
            "title": "Knowledge Representation and Logical Reasoning",
            "topics": [
                ("Definition and importance of knowledge", ["importance of knowledge", "why knowledge representation is important", "qualities of a good knowledge representation"]),
                ("Approaches to knowledge representation", ["approaches used in knowledge representation", "knowledge representation schemes", "types for knowledge representations", "instance and IS-A relationship", "is-a relationship"]),
                ("Issues in knowledge representation", ["issues in knowledge representation", "knowledge representation issues"]),
                ("Propositional logic", ["propositional logic", "syntax and semantics of propositional logic", "tautology", "satisfiable", "connectives"]),
                ("First Order Logic and inference", ["first order logic", "predicate logic", "FOL", "inference rules", "well-formed formula", "CNF", "converse inverse contrapositive"]),
                ("Forward and backward chaining", ["forward chaining", "backward chaining"]),
                ("Unification and resolution", ["unification", "resolution"]),
                ("Expert systems in PROLOG", ["expert system", "PROLOG", "prolog programming", "expert system architecture", "case study of expert system"]),
            ],
        },
        {
            "unit": "UNIT-III", "hours": 10,
            "title": "Handling Uncertainty and Natural Language Processing",
            "topics": [
                ("Non-monotonic reasoning", ["non-monotonic reasoning", "monotonic reasoning"]),
                ("Probabilistic reasoning and Bayes' theorem", ["probabilistic reasoning", "Bayes theorem", "Bayesian reasoning", "Bayesian networks"]),
                ("Certainty factors and rule-based systems", ["certainty factors", "rule-based systems"]),
                ("Dempster-Shafer theory", ["Dempster-Shafer"]),
                ("Fuzzy logic and fuzzy sets", ["fuzzy logic", "fuzzy set", "membership function", "crisp set", "fuzzification"]),
                ("NLP: syntactic processing", ["syntactic processing", "context-free grammar", "natural language parsers", "syntax"]),
                ("NLP: semantic processing", ["semantic processing", "semantics"]),
                ("NLP: pragmatic processing", ["pragmatic processing", "discourse integration", "discourse"]),
                ("NLP: introduction and applications", ["natural language processing", "NLP", "applications of NLP", "components of NLP", "steps in the process of natural language processing"]),
            ],
        },
        {
            "unit": "UNIT-IV", "hours": 10,
            "title": "Learning",
            "topics": [
                ("Introduction to learning", ["introduction to learning", "define learning in AI", "types of learning", "learning in problem solving"]),
                ("Rote learning", ["rote learning"]),
                ("Learning by taking advice", ["learning by taking advice"]),
                ("Learning from examples: induction", ["learning from examples", "induction", "inductive learning", "deductive and inductive"]),
                ("Explanation-based learning", ["explanation based learning", "explanation-based"]),
                ("Discovery", ["discovery"]),
                ("Analogy", ["analogy"]),
                ("Neural networks", ["neural network"]),
                ("Genetic learning", ["genetic learning", "genetic algorithm"]),
            ],
        },
    ],
}


def flat_topics() -> list[dict]:
    rows = []
    for unit in SYLLABUS["units"]:
        for name, aliases in unit["topics"]:
            rows.append({
                "topic": name, "unit": unit["unit"],
                "unit_hours": unit["hours"], "unit_title": unit["title"],
                "vocabulary": " ".join([name, *aliases]),
            })
    return rows
