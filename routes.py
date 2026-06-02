from fastapi import APIRouter
from database import SessionLocal
from  models  import Answer, Result, Summary

router = APIRouter()

# ------------------ ANSWER PIPELINE ------------------

@router.post("/submit-answer/")
def submit_answer(data: dict):
    db = SessionLocal()

    new_answer = Answer(
        candidate_id=data["candidate_id"],
        question_id=data["question_id"],
        answer=data["answer"],
        score=data.get("score", 0)
    )

    db.add(new_answer)
    db.commit()
    db.close()

    return {"message": "Answer stored successfully ✅"}


@router.get("/answers/")
def get_answers():
    db = SessionLocal()
    answers = db.query(Answer).all()
    db.close()
    return answers


# ------------------ RESULT PIPELINE ------------------

@router.post("/store-result/")
def store_result(data: dict):
    db = SessionLocal()

    result = Result(
        candidate_id=data["candidate_id"],
        total_score=data["total_score"],
        feedback=data["feedback"]
    )

    db.add(result)
    db.commit()
    db.close()

    return {"message": "Result stored successfully ✅"}


# ------------------ SUMMARY PIPELINE ------------------

@router.post("/store-summary/")
def store_summary(data: dict):
    db = SessionLocal()

    summary = Summary(
        candidate_id=data["candidate_id"],
        summary=data["summary"],
        recommendation=data["recommendation"]
    )

    db.add(summary)
    db.commit()
    db.close()

    return {"message": "Summary stored successfully ✅"}