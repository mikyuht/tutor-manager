import json

from tutor_ai import chat_json
from importlib import import_module

# Tên file bắt đầu bằng số nên không import thẳng được, dùng import_module
planner = import_module("05_planner")


def build_prompt(student, plan, lesson_minutes):
    lines = []
    for a in plan:
        lines.append(
            f'- {a["name"]}: {a["minutes"]} min, about {a["turns"]} student turns'
        )
    activity_text = "\n".join(lines)

    system = (
        "You are an experienced English speaking teacher. "
        "Write the content for each activity of a lesson plan. "
        "Use exactly the activity names given. Do not add or remove activities. "
        "Keep language suitable for the student's level. "
        "For each activity give: 'teacher_script' (what the teacher says or does, 1-2 sentences) "
        "and 'student_tasks' (a list of short prompts, questions or phrases for the student; "
        "about as many items as the student turns, but never more than 8). "
        'Reply only with JSON: {"activities": [{"name": "...", "teacher_script": "...", "student_tasks": ["..."]}]}'
    )
    user = (
        f"Student: level {student['level']}, goal: {student['goal']}, "
        f"interests: {student['interests']}, weak areas: {student['weak_areas']}\n"
        f"Lesson: {lesson_minutes} minutes, topic: {student['topic']}\n\n"
        f"Activities:\n{activity_text}"
    )
    return system, user


def fill_lesson(student, plan, lesson_minutes):
    system, user = build_prompt(student, plan, lesson_minutes)
    data = chat_json(system, user)

    # Code kiểm tra: chỉ nhận hoạt động có tên đúng
    by_name = {}
    for item in data.get("activities", []):
        by_name[item.get("name")] = item

    lesson = []
    for a in plan:
        item = by_name.get(a["name"], {})
        tasks = item.get("student_tasks", [])
        if isinstance(tasks, str):          # model đôi khi trả chuỗi thay vì list
            tasks = [tasks]
        lesson.append({
            "name": a["name"],
            "minutes": a["minutes"],
            "student_minutes": a["student_minutes"],
            "teacher_script": str(item.get("teacher_script", "")).strip()
                              or "(No content generated. Tutor to fill in.)",
            "student_tasks": [str(t) for t in tasks],
        })
    return lesson


if __name__ == "__main__":
    student = {
        "level": "B1",
        "goal": "Business meetings in English",
        "interests": "marketing, travel",
        "weak_areas": "hesitation, limited vocabulary for negotiation",
        "topic": "Negotiating a delivery date with a supplier",
    }
    minutes = 60

    plan = planner.build_plan(planner.BUSINESS_BLUEPRINT, minutes, 0.70)
    plan = planner.add_question_counts(plan, student["level"])
    lesson = fill_lesson(student, plan, minutes)

    for a in lesson:
        print(f'\n## {a["name"]} ({a["minutes"]} min, student {a["student_minutes"]} min)')
        print("Teacher:", a["teacher_script"])
        for t in a["student_tasks"]:
            print("  -", t)

    print(f'\nTong: {sum(a["minutes"] for a in lesson)} phut')