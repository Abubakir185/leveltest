from database import Session
from sqlalchemy import insert, select
from models import Level, Question
import json

session = Session()

with open("english_level_questions_abcd.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)


LEVEL_IDS = {
    "Beginner": 1,
    "Elementary": 2,
    "Pre-intermediate": 3,
    "Intermediate": 4
}

def add_level():
    session = Session()
    try:
        for name, id_ in LEVEL_IDS.items():
            exists = session.execute(
                select(Level).where(Level.name == name)
            ).first()
            if not exists:
                query = insert(Level).values(id=id_, name=name)
                session.execute(query)
        session.commit()
    finally:
        session.close()

def add_question():
    session = Session()
    try:
        for q in QUESTIONS:
            exists = session.execute(
                select(Question).where(Question.text == q["text"])
            ).first()
            if not exists:
                query = insert(Question).values(
                    level_id=q["level_id"],
                    text=q["text"],
                    option_a=next(opt["text"] for opt in q["options"] if opt["letter"] == "A"),
                    option_b=next(opt["text"] for opt in q["options"] if opt["letter"] == "B"),
                    option_c=next(opt["text"] for opt in q["options"] if opt["letter"] == "C"),
                    option_d=next(opt["text"] for opt in q["options"] if opt["letter"] == "D"),
                    correct_option=next(opt["letter"] for opt in q["options"] if opt["is_correct"])
                )
                session.execute(query)
        session.commit()
    finally:
        session.close()


