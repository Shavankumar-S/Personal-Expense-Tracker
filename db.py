from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker
import os

# Create SQLite DB in project folder
DB_PATH = "expenses.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Define table schema if not exists
metadata = MetaData()

expenses_table = Table(
    "expenses", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date, nullable=False),
    Column("category", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("description", String, nullable=True),
)

# Create tables if they don't exist
metadata.create_all(engine)

# Session factory
SessionLocal = sessionmaker(bind=engine)
