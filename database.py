import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError, InterfaceError, OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = (
    "postgresql+psycopg2://postgres:root@localhost:5432/ai_voice_interview"
)

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

DB_RETRY_ATTEMPTS = 3
DB_RETRY_DELAY_SECONDS = 2


def is_reconnectable_error(error):
    if isinstance(error, (OperationalError, InterfaceError)):
        return True

    if isinstance(error, DBAPIError) and error.connection_invalidated:
        return True

    return False


def retry_delay(attempt):
    return DB_RETRY_DELAY_SECONDS * attempt


def run_with_db_retry(operation, attempts=DB_RETRY_ATTEMPTS):
    last_error = None

    for attempt in range(1, attempts + 1):
        db = SessionLocal()
        try:
            result = operation(db)
            db.commit()
            return result
        except Exception as error:
            db.rollback()
            last_error = error

            if not is_reconnectable_error(error) or attempt == attempts:
                raise

            engine.dispose()
            print(
                "Database connection lost. "
                f"Retrying request ({attempt}/{attempts - 1})..."
            )
            time.sleep(retry_delay(attempt))
        finally:
            db.close()

    raise last_error


def create_tables_with_retry(metadata, attempts=DB_RETRY_ATTEMPTS):
    for attempt in range(1, attempts + 1):
        try:
            metadata.create_all(bind=engine)
            return
        except Exception as error:
            if not is_reconnectable_error(error) or attempt == attempts:
                raise

            engine.dispose()
            print(
                "Database is not ready at startup. "
                f"Retrying ({attempt}/{attempts - 1})..."
            )
            time.sleep(retry_delay(attempt))


def check_database_connection():
    def operation(db):
        db.execute(text("SELECT 1"))
        return {"database": "connected"}

    return run_with_db_retry(operation)
