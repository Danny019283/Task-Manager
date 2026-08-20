import os
from pathlib import Path
from typing import Iterator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
