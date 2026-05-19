import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
# Fall back to SQLite when the environment contains placeholder PostgreSQL values
if not DATABASE_URL or DATABASE_URL.startswith("postgresql://user:password"):
    DATABASE_URL = "sqlite:///./crm_hcp_db.sqlite"
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
