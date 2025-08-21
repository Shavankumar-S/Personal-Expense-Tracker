import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import sessionmaker

# --- Database setup ---
DATABASE_URL = "sqlite:///expenses.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

expenses_table = Table(
    "expenses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date),
    Column("category", String),
    Column("amount", Float),
    Column("description", String),
)

metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# --- Add Expense ---
def add_expense(date, category, amount, description):
    with SessionLocal() as session:
        session.execute(
            expenses_table.insert().values(
                date=date,
                category=category,
                amount=amount,
                description=description
            )
        )
        session.commit()

# --- Load Expenses ---
def load_expenses():
    df = pd.read_sql(expenses_table.select(), engine)
    return df

# --- Summary by Category ---
def get_summary():
    df = load_expenses()
    if df.empty:
        return pd.DataFrame(columns=["Category", "Amount"])
    
    summary = df.groupby("category", as_index=False)["amount"].sum()
    summary.rename(columns={"category": "Category", "amount": "Amount"}, inplace=True)
    return summary

# --- KPIs for Dashboard ---
def get_kpis():
    df = load_expenses()
    if df.empty:
        return {"total": 0, "average": 0, "max": 0}
    
    return {
        "total": df["amount"].sum(),
        "average": df["amount"].mean(),
        "max": df["amount"].max()
    }
