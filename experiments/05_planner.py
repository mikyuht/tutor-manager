# Blueprint: mỗi hoạt động có tên, % thời lượng bài, % học viên nói (mức cơ sở)
BUSINESS_BLUEPRINT = [
    ("Warm-up small talk",            0.10, 0.60),
    ("Key phrases (input)",           0.15, 0.20),
    ("Guided practice",               0.20, 0.60),
    ("Role-play",                     0.30, 0.85),
    ("Feedback and error correction", 0.15, 0.30),
    ("Wrap-up and homework",          0.10, 0.40),
]


def build_plan(blueprint, lesson_minutes, target_student_share):
    # Bước 1: chia phút theo tỉ lệ
    activities = []
    for name, share, student_share in blueprint:
        activities.append({
            "name": name,
            "minutes": round(lesson_minutes * share),
            "student_share": student_share,
        })

    # Bước 2: dịch chuyển tỉ lệ nói của mọi hoạt động cùng một lượng
    def weighted(shift):
        total = sum(a["minutes"] * min(0.95, max(0.10, a["student_share"] + shift))
                    for a in activities)
        return total / lesson_minutes

    # Tìm mức dịch (shift) bằng cách thử dần
    shift = 0.0
    for _ in range(200):
        diff = target_student_share - weighted(shift)
        if abs(diff) < 0.005:
            break
        shift += diff

    for a in activities:
        a["student_share"] = min(0.95, max(0.10, a["student_share"] + shift))
        a["student_minutes"] = round(a["minutes"] * a["student_share"], 1)

    return activities


# Độ dài trung bình một lượt nói của học viên (phút).
# Đây là số ƯỚC ĐOÁN, cần kiểm tra lại với gia sư thật.
ANSWER_MINUTES = {
    "A1": 0.4,
    "A2": 0.5,
    "B1": 0.75,
    "B2": 1.0,
    "C1": 1.5,
    "C2": 1.5,
}


def add_question_counts(activities, level):
    answer_len = ANSWER_MINUTES[level]
    for a in activities:
        count = round(a["student_minutes"] / answer_len)
        # Hoạt động nào học viên có nói thì ít nhất 1 lượt
        a["turns"] = max(1, count) if a["student_minutes"] > 0 else 0
    return activities


def print_plan(activities, lesson_minutes):
    total_min = sum(a["minutes"] for a in activities)
    total_student = sum(a["student_minutes"] for a in activities)
    for a in activities:
        print(f'{a["name"]:32} {a["minutes"]:>3} min   student {a["student_share"]*100:>3.0f}%  ({a["student_minutes"]} min)')
    print("-" * 70)
    print(f"Total: {total_min} min (muc tieu {lesson_minutes})")
    print(f"Student talk: {total_student:.1f} min = {total_student/lesson_minutes*100:.0f}%")


if __name__ == "__main__":
    for level in ["A2", "B1", "B2"]:
        print(f"\n=== Bai 60 phut, muc tieu 70%, trinh do {level} ===")
        plan = build_plan(BUSINESS_BLUEPRINT, 60, 0.70)
        plan = add_question_counts(plan, level)
        for a in plan:
            print(f'{a["name"]:32} {a["minutes"]:>3} min   '
                  f'student {a["student_minutes"]:>4} min   ~{a["turns"]} luot noi')