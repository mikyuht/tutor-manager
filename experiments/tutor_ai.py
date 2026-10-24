import json

import ollama

MODEL = "gemma4"  # must match `ollama list`


def chat_json(system, user):
    """Send instructions and data to the model, get a Python dictionary back."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        format="json",
        options={"temperature": 0, "num_ctx": 8192},
    )
    print(f"[model] total {response['total_duration']/1e9:.1f}s, load {response['load_duration']/1e9:.1f}s, "
          f"{response['eval_count']} tokens at {response['eval_count']/(response['eval_duration']/1e9):.0f} tok/s")
    return json.loads(response["message"]["content"])


ASSESS_SYSTEM = (
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
    "recurring_errors (list of short strings naming error patterns with a tiny example, "
    "for example: past simple, 'I go' instead of 'I went'), "
    "strengths (list of short strings), weaknesses (list of short strings), "
    "estimated_level (one of A1, A2, B1, B2, C1, C2), "
    "confidence (low, medium or high), "
    "recommended_focus (list of short strings)."
    )


def assess(text):
    return chat_json(ASSESS_SYSTEM, text)