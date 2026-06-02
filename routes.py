from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import is_reconnectable_error, run_with_db_retry
from models import Answer, Result, Summary

router = APIRouter()


def safe_db_operation(operation):
    try:
        return run_with_db_retry(operation)
    except Exception as error:
        if is_reconnectable_error(error):
            raise HTTPException(
                status_code=503,
                detail="Database connection failed after retries. Please try again.",
            )

        if isinstance(error, SQLAlchemyError):
            raise HTTPException(
                status_code=500,
                detail="Database operation failed.",
            )

        raise


@router.get("/health/db")
def database_health():
    def operation(db):
        db.execute(text("SELECT 1"))
        return {"database": "connected"}

    return safe_db_operation(operation)


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

    return safe_db_operation(operation)


@router.get("/answers/")
def get_answers():
    def operation(db):
        return db.query(Answer).all()

    return safe_db_operation(operation)


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

    return safe_db_operation(operation)


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

    return safe_db_operation(operation)
