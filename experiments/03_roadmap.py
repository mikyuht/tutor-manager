import json
import time

from tutor_ai import assess, chat_json

ROADMAP_SYSTEM = (
    "You design study roadmaps for an English tutor who teaches one speaking-focused session "
    "per week. Make a realistic plan that targets the student's goal and weaknesses, builds "
    "gradually from easier to harder, and ends with a review week. "
    "Reply only with JSON using these keys: "
    "summary (one or two sentences), "
    "weeks (list of objects with keys: week (number), goal (string), "
    "skills (list of strings), topics (list of strings))."
)


def make_roadmap(profile, assessment, weeks):
    user = (
        f"Student profile:\n{profile}\n\n"
        f"Assessment:\n{json.dumps(assessment, indent=2)}\n\n"
        f"Write exactly {weeks} weeks."
    )
    return chat_json(ROADMAP_SYSTEM, user)


PROFILE = """Goal: Business English speaking
Interests: marketing, football
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
print(json.dumps(roadmap, indent=2))
print(f"\nWeeks returned: {len(roadmap['weeks'])}")
print(f"Took {time.time() - start:.1f} seconds")