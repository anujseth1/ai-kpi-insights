import pandas as pd
import os
from pathlib import Path

def load_kpi_data(filepath):
    """
    Loads KPI data from a CSV file.
    Args:
        filepath (str): Path to the CSV file.
    Returns:
        pandas.DataFrame: DataFrame containing KPI data.
    """
    file_path_obj = Path(filepath).resolve()
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File {file_path_obj} not found.")
    
    df = pd.read_csv(file_path_obj)
    
    expected_columns = ['date', 'revenue', 'new_users', 'active_users', 'refunds', 'conversion_rate']
    if not all(col in df.columns for col in expected_columns):
        raise ValueError(f"Data is missing expected columns. Found columns: {df.columns.tolist()}")
    
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Loaded {len(df)} rows of data from {file_path_obj}.")
    return df


# Quick test
if __name__ == "__main__":
    # Always resolve path relative to this script
    script_dir = Path(__file__).parent
    data_path = script_dir.parent / "data" / "sample_kpi_data.csv"
    
    df = load_kpi_data(data_path)
    print(df.head())


import sqlalchemy

def load_kpi_from_sql(query, db_url):
    """
    Loads KPI data from a SQL database.
    Args:
        query (str): SQL query to run.
        db_url (str): SQLAlchemy database URL.
    Returns:
        pandas.DataFrame: DataFrame containing KPI data.
    """
    engine = sqlalchemy.create_engine(db_url)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    df['date'] = pd.to_datetime(df['date'])
    print(f"Loaded {len(df)} rows of data from database.")
    return df
