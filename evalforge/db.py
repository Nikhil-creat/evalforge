import pandas as pd
from sqlalchemy import create_engine, inspect
from .config import DB_URL
engine = create_engine(DB_URL, future=True)

def read(table):
    return pd.read_sql_table(table, engine) if inspect(engine).has_table(table) else pd.DataFrame()

def write(df, table, mode="append"):
    df.to_sql(table, engine, if_exists=mode, index=False)
