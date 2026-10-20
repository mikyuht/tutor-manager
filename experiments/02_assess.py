import json

import ollama

SYSTEM = (
    "You are an experienced English teacher. You get a transcript of a student speaking, "
    "or a tutor's notes about the student. Estimate the speaking level using these guidelines. "
    "A1: isolated words and memorised phrases. "
    "A2: simple sentences about familiar topics, short pauses and frequent basic errors, "
    "but gets simple messages across. "
    "B1: connects ideas to describe experiences, give reasons, opinions and plans, with some "
    "hesitation. Tense and word-choice errors are common but the meaning is usually clear. "
    "B2: speaks fairly fluently and spontaneously, gives detailed explanations, errors are "
    "occasional and rarely block understanding. "
    "C1 and C2: fluent, flexible and precise, with natural phrasing. "
    "Do not lower the level just because of grammar mistakes. Judge mostly how well the student "
    "gets meaning across and how long and connected the answers are. "
    "Base every claim on the input and do not invent facts. "
    "Reply only with JSON using these keys, in this order: "
    "evidence (list of short quotes or observations from the input), "
    "strengths (list of short strings), weaknesses (list of short strings), "
    "estimated_level (one of A1, A2, B1, B2, C1, C2), "
    "confidence (low, medium or high), "
    "recommended_focus (list of short strings)."
)


def assess(text):
    response = ollama.chat(
        model="gemma4",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": text},
        ],
        format="json",
    )
    return json.loads(response["message"]["content"])


SAMPLE = """
Yesterday I go to the office and I have meeting with my boss. He say me that I must
finishing the report before Friday. I am very nervous because, um, my English is not
very good and I don't know how to say... presentation? I want to speak with clients
more confident. I work in marketing three years.
"""

result = assess(SAMPLE)
print(json.dumps(result, indent=2))