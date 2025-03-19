import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df, feature_column='revenue', contamination=0.05):
    """
    Detects anomalies in a KPI column using Isolation Forest.
    Args:
        df (pd.DataFrame): KPI data.
        feature_column (str): The column on which to detect anomalies.
        contamination (float): Proportion of expected anomalies.
    Returns:
        pd.DataFrame: Data with anomaly flags.
    """
    print(f"Running anomaly detection on '{feature_column}'...")
    
    model = IsolationForest(contamination=contamination, random_state=42)
    df['anomaly_score'] = model.fit_predict(df[[feature_column]])
    df['is_anomaly'] = df['anomaly_score'].apply(lambda x: 'Yes' if x == -1 else 'No')
    
    anomaly_count = df['is_anomaly'].value_counts().get('Yes', 0)
    print(f"Detected {anomaly_count} anomalies out of {len(df)} rows.")
    
    return df


# Quick test
if __name__ == "__main__":
    from pathlib import Path
    from data_ingestion import load_kpi_data
    from preprocessing import clean_kpi_data
    
    script_dir = Path(__file__).parent
    data_path = script_dir.parent / "data" / "sample_kpi_data.csv"
    
    df = load_kpi_data(data_path)
    df = clean_kpi_data(df)
    
    df = detect_anomalies(df, feature_column='revenue')
    print(df[df['is_anomaly'] == 'Yes'])
