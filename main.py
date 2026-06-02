from fastapi import FastAPI

from database import Base, create_tables_with_retry
from routes import router

app = FastAPI()

try:
    create_tables_with_retry(Base.metadata)
    print("Database connected and tables created successfully")
except Exception as e:
    print(f"Database connection failed after retries: {e}")
    print("Please ensure:")
    print("   1. PostgreSQL is running")
    print("   2. Database 'ai_voice_interview' exists")
    print("   3. Credentials are correct (postgres:root@localhost:5432)")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Backend is running"}
