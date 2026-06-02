import time

from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError, OperationalError
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

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DB_RETRY_ATTEMPTS = 3
DB_RETRY_DELAY_SECONDS = 2


def is_reconnectable_error(error):
    return isinstance(error, OperationalError) or (
        isinstance(error, DBAPIError) and error.connection_invalidated
    )


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
                f"Database connection lost. Reconnecting "
                f"({attempt}/{attempts - 1})..."
            )
            time.sleep(DB_RETRY_DELAY_SECONDS)
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
                f"Database startup connection failed. Retrying "
                f"({attempt}/{attempts - 1})..."
            )
            time.sleep(DB_RETRY_DELAY_SECONDS)
