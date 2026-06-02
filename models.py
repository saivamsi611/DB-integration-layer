from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from database import Base

# Candidate Table
class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    skills = Column(Text)


# Question Table
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    difficulty = Column(String)
    role = Column(String)


# Answer Table
class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer = Column(Text)
    score = Column(Float)


# Result Table
class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer)
    total_score = Column(Float)
    feedback = Column(Text)


# Summary Table
class Summary(Base):
    __tablename__ = "summary"
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer)
    summary = Column(Text)
    recommendation = Column(String) 