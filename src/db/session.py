from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
import os

# Exemple : postgresql://username:password@hostname:port/dbname
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caisse"
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
