"""Natural Language Processing syllabus (new subject, no past papers exist).

This is the "cold start" case: a subject introduced this year. There is no
history to rank by, so the product must be honest about what it can offer.

Teaching hours are recorded per unit because, absent PYQs, they are the only
weighting signal the university itself provides.
"""

SYLLABUS = {
    "subject": "Natural Language Processing",
    "year": 2025,
    "has_past_papers": False,
    "units": [
        {
            "unit": "UNIT-I", "hours": 12,
            "title": "Introduction to NLP and Text Preprocessing",
            "topics": [
                ("Scope, challenges and applications of NLP", ["scope of NLP", "challenges in NLP", "applications of natural language processing"]),
                ("Levels of language processing", ["morphological", "lexical", "syntactic", "semantic", "discourse", "levels of language processing", "pragmatic"]),
                ("Tokenization", ["tokenization", "tokens", "word tokenization"]),
                ("Normalization", ["normalization", "text normalization", "case folding"]),
                ("Stemming", ["stemming", "porter stemmer"]),
                ("Lemmatization", ["lemmatization", "lemma"]),
                ("Stop-word removal", ["stop word removal", "stopwords"]),
                ("Regular expressions", ["regular expressions", "regex", "pattern matching"]),
            ],
        },
        {
            "unit": "UNIT-II", "hours": 12,
            "title": "POS Tagging, Parsing and Language Models",
            "topics": [
                ("Part-of-Speech tagging", ["part of speech tagging", "POS tagging", "pos tagger"]),
                ("Context-Free Grammar and syntactic parsing", ["context free grammar", "CFG", "syntactic parsing", "parse tree", "parsing"]),
                ("Named Entity Recognition", ["named entity recognition", "NER", "entity extraction"]),
                ("Word Sense Disambiguation", ["word sense disambiguation", "WSD", "word sense"]),
                ("Language models and n-grams", ["language model", "n-gram", "ngram", "bigram", "trigram"]),
            ],
        },
        {
            "unit": "UNIT-III", "hours": 12,
            "title": "Feature Extraction and Text Classification",
            "topics": [
                ("Feature extraction: need and importance", ["feature extraction", "features from text", "importance of feature extraction"]),
                ("Bag of Words", ["bag of words", "BoW", "count vectorizer"]),
                ("TF-IDF", ["TF-IDF", "term frequency", "inverse document frequency"]),
                ("Text classification using Naive Bayes", ["naive bayes", "text classification", "classifier"]),
                ("Sentiment analysis", ["sentiment analysis", "opinion mining", "polarity"]),
                ("Information extraction", ["information extraction", "relation extraction"]),
                ("Text summarization", ["text summarization", "summarization", "extractive summary"]),
            ],
        },
        {
            "unit": "UNIT-IV", "hours": 10,
            "title": "Embeddings, Deep Learning and LLMs",
            "topics": [
                ("Word embeddings: Word2Vec", ["word embeddings", "word2vec", "embedding", "vector representation of words"]),
                ("Deep learning for NLP", ["deep learning for NLP", "neural network for text", "RNN", "LSTM"]),
                ("Transformers and Large Language Models", ["transformer", "large language model", "LLM", "attention", "BERT", "GPT"]),
                ("Applications: machine translation", ["machine translation", "translation"]),
                ("Applications: question answering", ["question answering", "QA system"]),
                ("Applications: chatbots and speech assistants", ["chatbot", "speech assistant", "dialogue system", "conversational agent"]),
                ("Applications: generative AI", ["generative AI", "text generation", "generative model"]),
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


if __name__ == "__main__":
    topics = flat_topics()
    total_hours = sum(u["hours"] for u in SYLLABUS["units"])
    print(f"{SYLLABUS['subject']} - {len(topics)} topics, {total_hours} teaching hours")
    print("past papers available:", SYLLABUS["has_past_papers"])
    print()
    for u in SYLLABUS["units"]:
        share = u["hours"] / total_hours
        print(f"  {u['unit']}  {u['hours']:2d}h ({share:4.0%})  {len(u['topics'])} topics  {u['title']}")
