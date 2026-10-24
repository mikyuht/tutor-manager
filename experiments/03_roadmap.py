import json
import time

from tutor_ai import assess, chat_json

ROADMAP_SYSTEM = (
    "You design study roadmaps for an English tutor who teaches speaking-focused sessions. "
    "Pacing: pitch the plan at the student's current CEFR level. Weeks 1 and 2 consolidate that "
    "level, and only the last third may stretch toward the next level. Never plan tasks more than "
    "one level above the current one. "
    "Specificity: every week must have a DIFFERENT language focus. Take the student's recurring "
    "errors and assign each one to a week, naming the exact structure (for example: past simple "
    "irregular verbs). Never use vague labels such as 'Speaking', 'Grammar' or 'Fluency' as a focus. "
    "Mention the student's interests in at most two weeks, and only where natural. "
    "The last week reviews the earlier focuses. "
    "Reply only with JSON using these keys: "
    "summary (one sentence), "
    "weeks (list of objects with keys: week (number), "
    "focus (the specific language target, under 12 words), "
    "speaking_task (what the student does out loud, one sentence), "
    "success_check (an observable sign it worked, one sentence), "
    "homework (one task of at most 10 minutes))."
)


def make_roadmap(profile, assessment, weeks):
    user = (
        f"Student profile:\n{profile}\n\n"
        f"Current level: {assessment.get('estimated_level') or 'unknown'}\n"
        f"Weaknesses: {'; '.join(assessment.get('weaknesses', []))}\n"
        f"Recurring errors: {'; '.join(assessment.get('recurring_errors', []))}\n"
        f"Recommended focus: {'; '.join(assessment.get('recommended_focus', []))}\n\n"
        f"Write exactly {weeks} weeks."
    )
    return chat_json(ROADMAP_SYSTEM, user)

def check_roadmap(roadmap, interests):
    """Cheap code checks on the model's output. Returns a list of problems."""
    problems = []
    weeks = roadmap.get("weeks", [])
    focuses = [str(w.get("focus", "")).lower() for w in weeks]
    if len(set(focuses)) < len(focuses):
        problems.append("Some weeks repeat the same focus.")
    for word in interests:
        count = sum(word.lower() in json.dumps(w).lower() for w in weeks)
        if count > 2:
            problems.append(f"'{word}' appears in {count} weeks.")
    return problems


PROFILE = """Goal: Business English speaking
Interests: accounting, hiking
Weak areas: fluency, vocabulary
Sessions: one 60-minute session per week"""

SAMPLE = """
Yesterday I go to the office and I have meeting with my boss. He say me that I must
finishing the report before Friday. I am very nervous because, um, my English is not
very good and I don't know how to say... presentation? I want to speak with clients
more confident. I work in marketing three years.
"""

start = time.time()
assessment = assess(SAMPLE)
roadmap = make_roadmap(PROFILE, assessment, 6)

print(json.dumps(assessment, indent=2))
print(json.dumps(roadmap, indent=2))
print("Problems:", check_roadmap(roadmap, ["football"]) or "none")
print(f"\nWeeks returned: {len(roadmap['weeks'])}")
print(f"Took {time.time() - start:.1f} seconds")

