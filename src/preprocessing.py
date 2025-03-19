import pandas as pd

def clean_kpi_data(df):
    """
    Cleans the KPI DataFrame.
    Steps:
    - Remove rows with missing values
    - Ensure 'date' column is datetime
    - Sort data by date
    """
    initial_count = len(df)
    df = df.dropna()  # Remove missing values
    cleaned_count = len(df)
    removed = initial_count - cleaned_count
    if removed > 0:
        print(f"Removed {removed} rows with missing values.")
    
    # Ensure correct data types
    if df['date'].dtype != 'datetime64[ns]':
        df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values(by='date').reset_index(drop=True)
    
    print(f"Cleaned data: {len(df)} rows ready for analysis.")
    return df


# Quick test
if __name__ == "__main__":
    from pathlib import Path
    from data_ingestion import load_kpi_data
    
    script_dir = Path(__file__).parent
    data_path = script_dir.parent / "data" / "sample_kpi_data.csv"
    df = load_kpi_data(data_path)
    
    cleaned_df = clean_kpi_data(df)
    print(cleaned_df.head())
