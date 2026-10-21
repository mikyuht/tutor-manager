import json
from pathlib import Path

from tutor_ai import chat_json


def load_books():
    # Đường dẫn tới data/books.json, tính từ vị trí của file này
    path = Path(__file__).parent.parent / "data" / "books.json"
    return json.loads(path.read_text(encoding="utf-8"))


def filter_books(books, level, skill):
    # Giữ lại sách nào có level và skill khớp
    return [b for b in books if level in b["levels"] and skill in b["skills"]]


def explain_books(student, candidates):
    # Model chỉ nhìn thấy các sách đã lọc, kèm id
    catalog_text = "\n".join(
        f'- id: {b["id"]} | {b["title"]} | focus: {b["focus"]}' for b in candidates
    )

    system = (
        "You are an experienced English teacher. "
        "For each book in the list, explain in 1-2 short sentences why it fits this student. "
        "Use ONLY the books in the list. Do not add other books. "
        'Reply only with JSON: {"picks": [{"id": "...", "why": "..."}]}'
    )
    user = (
        f"Student: level {student['level']}, goal: {student['goal']}, "
        f"interests: {student['interests']}, weak areas: {student['weak_areas']}\n\n"
        f"Books:\n{catalog_text}"
    )

    data = chat_json(system, user)
    # Code kiểm tra: chỉ giữ id có thật trong danh sách đã lọc
    allowed = {b["id"]: b for b in candidates}
    why_by_id = {}
    for pick in data.get("picks", []):
        if pick.get("id") in allowed:
            why_by_id[pick["id"]] = str(pick.get("why", "")).strip()

    # Sách nào model bỏ sót thì có câu dự phòng, để không bị trống
    results = []
    for b in candidates:
        why = why_by_id.get(b["id"]) or "(No explanation generated. Tutor to decide.)"
        results.append({"id": b["id"], "title": b["title"], "why": why})
    return results


if __name__ == "__main__":
    books = load_books()

    student = {
        "level": "B1",
        "goal": "Business meetings in English",
        "interests": "marketing, travel",
        "weak_areas": "hesitation, limited vocabulary for negotiation",
    }

    candidates = filter_books(books, student["level"], "business")
    print(f"Sau khi loc: {len(candidates)} sach\n")

    if not candidates:
        print("Chua co sach phu hop trong danh muc.")
    else:
        for r in explain_books(student, candidates):
            print(f"- {r['title']}\n  {r['why']}\n")