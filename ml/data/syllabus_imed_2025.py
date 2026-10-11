"""Introduction to Management and Entrepreneurship Development (BCA-206) syllabus."""

SYLLABUS = {
    "subject": "Management & Entrepreneurship",
    "code": "BCA-206",
    "year": 2025,
    "units": [
        {
            "unit": "UNIT-I", "hours": 10,
            "title": "Introduction to Entrepreneurship",
            "topics": [
                ("Meaning and concept of entrepreneurship", ["meaning and concept of entrepreneurship", "define entrepreneurship", "how would you define an entrepreneurship", "what is entrepreneurship"]),
                ("History of entrepreneurship development", ["history of entrepreneurship development", "historical evolution of entrepreneurship", "state of entrepreneurship in India", "early years of independence"]),
                ("Role of entrepreneurship in economic development", ["role of entrepreneurship in economic development", "economic development of a country", "roles to be played by entrepreneurs", "country's economy"]),
                ("Characteristics and personality traits of entrepreneurs", ["general characteristics and personality traits", "personality traits", "skills required to be an entrepreneur", "types of entrepreneurs", "Clarence Danhof", "intrapreneur"]),
                ("Factors affecting entrepreneurship", ["factors affecting entrepreneurship", "factors that affect the growth", "challenges faced by an entrepreneur"]),
                ("Agencies in entrepreneurship development in India", ["agencies that support entrepreneurship development", "agencies in entrepreneurship development", "public agencies", "private agencies", "NIESBUD", "SIDBI", "MSME"]),
            ],
        },
        {
            "unit": "UNIT-II", "hours": 10,
            "title": "Creativity and Innovation",
            "topics": [
                ("Necessity of creativity", ["necessity of creativity", "what is creativity", "creativity in entrepreneurial development", "creativity and innovation contribute"]),
                ("Steps in creativity", ["steps of creativity", "process and steps of creativity", "steps involved in the creative process", "creative process"]),
                ("Defining innovation and its importance", ["what is innovation", "define innovation", "importance of innovation", "stages of innovation", "process and steps of innovation", "hindrances to innovation"]),
                ("Identification of opportunities through innovation", ["identification of opportunities", "problem solving with innovation", "creative problem solving", "innovative decision-making", "SWOT analysis"]),
                ("Decision making and problem solving", ["decision making", "problem solving", "steps in decision making", "creative thinking and decision-making"]),
                ("Examples from industry and day-to-day operations", ["example from industry", "day-to-day operational activities", "real-life case from any industry"]),
            ],
        },
        {
            "unit": "UNIT-III", "hours": 10,
            "title": "Role of an Entrepreneur",
            "topics": [
                ("Entrepreneur's contribution to society", ["contribution to society", "social responsibility of business", "impact of entrepreneurs"]),
                ("Changing mindset and out-of-box thinking", ["out-of-box thinking", "out-of-the-box thinking", "changing mindset", "changing the mindset"]),
                ("Design thinking", ["design thinking", "stages of design thinking", "objectives of design thinking"]),
                ("Entrepreneurs as role models, mentors and influencers", ["role model", "mentor", "influencer", "entrepreneurs as role models", "budding business minds"]),
                ("Entrepreneurial success stories", ["success stories", "journey to success", "achieved success"]),
                ("Global Indian entrepreneurs and modern entrepreneurs", ["global entrepreneurs", "global Indian entrepreneurs", "modern entrepreneurs", "traditional entrepreneurs", "across the globe"]),
            ],
        },
        {
            "unit": "UNIT-IV", "hours": 10,
            "title": "Fundamentals of Management",
            "topics": [
                ("Meaning of business and its management", ["meaning of business", "business and its management", "entrepreneurship and business", "roles of entrepreneurs and managers", "entrepreneur and manager"]),
                ("Role and importance of leadership", ["role and importance of leadership", "importance of leadership", "leadership in entrepreneurship", "leadership influence business success", "can leadership be developed"]),
                ("Difference between management and leadership", ["difference between leadership and management", "management different from leadership"]),
                ("Importance of planning in a venture", ["importance of planning", "planning and managing their ventures", "challenges faced by entrepreneurs in planning"]),
                ("Role and importance of a business plan", ["business plan", "significance in entrepreneurship", "components of a comprehensive business plan", "roadmap for entrepreneurs"]),
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
