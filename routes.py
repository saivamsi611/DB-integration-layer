from fastapi import APIRouter

from database import run_with_db_retry
from models import Answer, Result, Summary

router = APIRouter()


@router.post("/submit-answer/")
def submit_answer(data: dict):
    def operation(db):
        new_answer = Answer(
            candidate_id=data["candidate_id"],
            question_id=data["question_id"],
            answer=data["answer"],
            score=data.get("score", 0),
        )
        db.add(new_answer)
        return {"message": "Answer stored successfully"}

    return run_with_db_retry(operation)


@router.get("/answers/")
def get_answers():
    def operation(db):
        return db.query(Answer).all()

    return run_with_db_retry(operation)


@router.post("/store-result/")
def store_result(data: dict):
    def operation(db):
        result = Result(
            candidate_id=data["candidate_id"],
            total_score=data["total_score"],
            feedback=data["feedback"],
        )
        db.add(result)
        return {"message": "Result stored successfully"}

    return run_with_db_retry(operation)


@router.post("/store-summary/")
def store_summary(data: dict):
    def operation(db):
        summary = Summary(
            candidate_id=data["candidate_id"],
            summary=data["summary"],
            recommendation=data["recommendation"],
        )
        db.add(summary)
        return {"message": "Summary stored successfully"}

    return run_with_db_retry(operation)
