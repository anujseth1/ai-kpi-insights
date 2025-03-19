import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from anomaly_detection import detect_anomalies
from data_ingestion import load_kpi_data
from preprocessing import clean_kpi_data
from pathlib import Path

def plot_kpi_with_anomalies(df, kpi_column):
    """
    Plot time series for a KPI column with anomalies marked in red.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['date'], df[kpi_column], label=kpi_column, linewidth=2)
    
    anomalies = df[df['is_anomaly'] == 'Yes']
    ax.scatter(anomalies['date'], anomalies[kpi_column], color='red', label='Anomaly', s=80)
    
    ax.set_title(f"{kpi_column.title()} Over Time with Anomalies")
    ax.set_xlabel("Date")
    ax.set_ylabel(kpi_column.title())
    ax.legend()
    st.pyplot(fig)


def main():
    st.title("📈 Business KPI Anomaly Dashboard")
    
    # Load and clean data
    script_dir = Path(__file__).parent
    data_path = script_dir.parent / "data" / "sample_kpi_data.csv"
    df = load_kpi_data(data_path)
    df = clean_kpi_data(df)
    
    kpi_columns = ['revenue', 'new_users', 'active_users', 'refunds', 'conversion_rate']
    kpi_selected = st.selectbox("Select KPI to Analyze", kpi_columns)
    
    contamination_level = st.slider("Anomaly Sensitivity (Contamination %)", 0.01, 0.20, 0.05, 0.01)
    
    # Detect anomalies
    df = detect_anomalies(df, feature_column=kpi_selected, contamination=contamination_level)
    
    # Plot KPI
    plot_kpi_with_anomalies(df, kpi_selected)
    
    # Show anomaly table
    st.subheader("Anomalies Detected:")
    st.dataframe(df[df['is_anomaly'] == 'Yes'][['date', kpi_selected]])


if __name__ == "__main__":
    main()
