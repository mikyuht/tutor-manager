from tutor_ai import chat_json

MODES = ["vocab_focus", "discussion_focus", "mixed"]


def choose_mode(student, recent_notes="", forced_mode=None):
    # Tutor ghi đè thì bỏ qua model
    if forced_mode in MODES:
        return {"mode": forced_mode, "reason": "Chosen by tutor.", "by": "tutor"}

    system = (
        "You are an experienced English speaking teacher planning ONE lesson. "
        "Choose the lesson mode that fits this student today. Modes:\n"
        "- vocab_focus: student lacks words/phrases for the topic, or the topic is new. "
        "Lesson teaches about 6 phrases first, then practises them.\n"
        "- discussion_focus: student has enough words but hesitates or needs fluency. "
        "Lesson is mostly questions, discussion and role-play, no new vocabulary table.\n"
        "- mixed: not clear, or both needs are present.\n"
        "Use only the evidence given. If there is little evidence, choose mixed. "
        'Reply only with JSON: {"mode": "vocab_focus|discussion_focus|mixed", '
        '"reason": "one short sentence"}'
    )
    user = (
        f"Student: level {student['level']}, goal: {student['goal']}, "
        f"weak areas: {student['weak_areas']}, lesson topic: {student['topic']}\n"
        f"Recent tutor notes: {recent_notes or '(none)'}"
    )
    data = chat_json(system, user)

    mode = str(data.get("mode", "")).strip()
    if mode not in MODES:          # code kiểm tra
        return {"mode": "mixed", "reason": "Model answer invalid, default used.", "by": "fallback"}
    return {"mode": mode, "reason": str(data.get("reason", "")).strip(), "by": "model"}


if __name__ == "__main__":
    base = {
        "level": "B1",
        "goal": "Business meetings in English",
        "topic": "Negotiating a delivery date with a supplier",
    }
    tests = [
        ({**base, "weak_areas": "limited vocabulary for negotiation"}, ""),
        ({**base, "weak_areas": "hesitation, long pauses"},
         "Last lesson: knew the key phrases well but froze in role-play."),
        ({**base, "weak_areas": ""}, ""),
    ]
    for student, notes in tests:
        r = choose_mode(student, notes)
        print(f"{r['mode']:18} ({r['by']})  {r['reason']}")