from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import config


engine = create_engine(config.DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """
    The get_db function is a context manager that returns the database session.
    It also ensures that the connection to the database is closed after each request.

    :return: A database session
    :doc-author: Trelent
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
