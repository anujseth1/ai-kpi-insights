import pandas as pd
from pathlib import Path
from data_ingestion import load_kpi_data
from preprocessing import clean_kpi_data
from anomaly_detection import detect_anomalies

def main():
    print("🚀 Starting KPI monitoring agent...")

    # Step 1: Load and clean data
    script_dir = Path(__file__).parent
    data_path = script_dir.parent / "data" / "sample_kpi_data.csv"
    df = load_kpi_data(data_path)
    df = clean_kpi_data(df)

    # Step 2: List KPIs to check
    kpi_columns = ['revenue', 'new_users', 'active_users', 'refunds', 'conversion_rate']

    # Step 3: Run anomaly detection for each KPI
    summary_report = []
    for kpi in kpi_columns:
        print(f"\n➡️ Detecting anomalies for: {kpi}")
        result_df = detect_anomalies(df.copy(), feature_column=kpi, contamination=0.05)
        anomalies_found = result_df[result_df['is_anomaly'] == 'Yes']
        summary_report.append((kpi, len(anomalies_found)))
        
        # Save result CSV for each KPI
        output_file = script_dir.parent / "data" / f"{kpi}_anomalies_output.csv"
        anomalies_found[['date', kpi]].to_csv(output_file, index=False)
        print(f"Saved anomalies for {kpi} in {output_file}")

    # Step 4: Print summary
    print("\n📊 Anomaly Detection Summary:")
    for kpi, count in summary_report:
        print(f"{kpi.title()}: {count} anomalies detected")

    print("\n✅ Monitoring run complete. Reports saved in /data folder.")


if __name__ == "__main__":
    main()
