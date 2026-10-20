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
    return json.loads(response["message"]["content"])


ASSESS_SYSTEM = "PASTE YOUR CALIBRATED SYSTEM PROMPT FROM 02_assess.py HERE"


def assess(text):
    return chat_json(ASSESS_SYSTEM, text)