from tutor_ai import chat_json

import re



def norm(text):
    # Chữ thường, đổi ’ thành ', bỏ dấu câu (giữ dấu nháy đơn trong từ như Let's)
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^\w' ]+", " ", text)
    return " ".join(text.split())

def make_vocab(student, count=6):
    system = (
        f"You are an English teacher. Choose {count} useful phrases for ONE lesson. "
        f"Everything you write must be easy for a CEFR {student['level']} learner: "
        "short sentences, common words, no rare idioms. "
        "For each phrase give: "
        "'phrase', "
        "'definition' (max 10 words, simpler than the phrase itself), "
        "'examples' (exactly 2 sentences using the phrase, max 12 words each), "
        "'question' (ONE speaking prompt, max 25 words. Choose one of two styles: "
        "(a) a line said by the other person in a work situation, followed by 'Your reply?', "
        "e.g. Supplier: \"We can't deliver before the 28th.\" Your reply? "
        "(b) a question about the student's own work experience, "
        "e.g. 'Tell me about a time a deadline was too tight. What did you do?'. "
        "Use a mix of both styles across the phrases. "
        "Never name the function of the phrase: do NOT write 'How do you ask for...', "
        "'How do you say...', or 'How do you show...'. "
        "The prompt must NOT contain the phrase itself, and must not be a yes/no question)."
        "The prompt must NOT contain the phrase itself, and must not be a yes/no question). "
        'Reply only with JSON: {"items": [{"phrase": "...", "definition": "...", '
        '"examples": ["...", "..."], "question": "..."}]}'
    )
    user = (
        f"Student goal: {student['goal']}. Interests: {student['interests']}. "
        f"Weak areas: {student['weak_areas']}. Lesson topic: {student['topic']}."
    )
    data = chat_json(system, user)
    print("KEYS:", list(data.keys()))
    print(str(data)[:600])

    items = []
    for it in data.get("items", []):
        examples = it.get("examples", [])
        if isinstance(examples, str):
            examples = [examples]
        phrase = str(it.get("phrase", "")).strip()
        if not phrase:
            continue
        items.append({
            "phrase": phrase,
            "definition": str(it.get("definition", "")).strip(),
            "examples": [str(e).strip() for e in examples][:2],
            "question": str(it.get("question", "")).strip(),
        })
    return items[:count]


if __name__ == "__main__":
    student = {
        "level": "B1",
        "goal": "Business meetings in English",
        "interests": "marketing, travel",
        "weak_areas": "hesitation, limited vocabulary for negotiation",
        "topic": "Negotiating a delivery date with a supplier",
    }
    items = make_vocab(student)
    print(f"\nNhan duoc {len(items)} cum tu\n")
    for it in items:
        print(f"* {it['phrase']}")
        print(f"  Definition: {it['definition']}")
        for e in it["examples"]:
            print(f"  Example: {e}")
        print(f"  Question: {it['question']}")
        # Code kiểm tra: ví dụ có thật sự chứa cụm từ không?
        p = norm(it["phrase"])
        if not all(p in norm(e) for e in it["examples"]):
            print("  [!] Co vi du khong chua dung cum tu, tutor can xem lai")
        if not it["question"].endswith("?"):
            print("  [!] Cau hoi khong ket thuc bang dau ?")
        if p in norm(it["question"]):
            print("  [!] Cau hoi da chua san cum tu, hoc vien chi can doc lai")
        q = it["question"].lower()
        if q.startswith(("how do you ask", "how do you say", "how do you show", "how do you offer")):
            print("  [!] Cau hoi van noi thang chuc nang cua cum tu")