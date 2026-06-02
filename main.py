from fastapi import FastAPI
from database import engine, Base
from routes import router
app = FastAPI()
# create tables
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database connected and tables created successfully")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("⚠️ Please ensure:")
    print("   1. PostgreSQL is running")
    print("   2. Database 'ai_voice_interview' exists")
    print("   3. Credentials are correct (postgres:root@localhost:5432)")
#include roots
app.include_router(router)
@app.get("/")
def home():
    return {"message": "Backend is running"}