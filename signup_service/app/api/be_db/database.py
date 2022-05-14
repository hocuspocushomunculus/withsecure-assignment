from sqlmodel import SQLModel, create_engine
import os

sqlite_file_name = "be_db.db"
DATABASE_URI = os.getenv("DATABASE_URI", f"sqlite:///{sqlite_file_name}")

engine = create_engine(DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
