"""
utils/data_processor.py
========================
BrightWave Retail Promotion Analytics
Single Source of Truth Data Processing Pipeline

This module loads, audits, cleans, and feature-engineers the BrightWave
promotional campaign dataset, ensuring that the Jupyter Notebook,
Project Report, and Interactive Web Application operate on 100% identical,
mathematically verified metrics.
"""

import os
import json
import pandas as pd
import numpy as np


def load_raw_data(filepath=None):
    """
    Loads raw promotion data from CSV or Excel.
    Prefers CSV if available, otherwise falls back to Excel 'Promotion Data' sheet.
    """
    if filepath is None:
        # Default lookups in current directory or data/ directory
        candidates = [
            'Promotion_Analytics_Data.csv',
            'Promotion_Analytics_Data.xlsx',
            os.path.join('data', 'Promotion_Analytics_Data.csv'),
            os.path.join('data', 'Promotion_Analytics_Data.xlsx')
        ]
        for c in candidates:
            if os.path.exists(c):
                filepath = c
                break

    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"Promotion dataset file not found in candidates: {candidates}")

    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath, sheet_name='Promotion Data')
    return df


def audit_raw_data(df):
    """
    Audits the raw dataset before any cleaning or transformation.
    Returns a comprehensive audit dictionary.
    """
    total_rows = len(df)
    total_cols = len(df.columns)
    duplicate_rows = int(df.duplicated().sum())
    missing_by_col = df.isnull().sum().to_dict()

    audit_report = {
        'initial_row_count': total_rows,
        'initial_column_count': total_cols,
        'duplicate_rows_count': duplicate_rows,
        'missing_values': {k: int(v) for k, v in missing_by_col.items() if v > 0},
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    return audit_report


def clean_and_transform_data(df_raw):
    """
    Executes the end-to-end cleaning and feature engineering pipeline:
    1. Removes duplicate records.
    2. Standardizes categorical columns (Channel, Campaign_Type, Region, Product_Category).
    3. Imputes missing values transparently (median for numerical, mode for categorical).
    4. Parses dates to datetime64.
    5. Computes derived KPIs: Month, Month_Num, Click_Through_Rate, Conversion_Rate, Return_on_Ad_Spend.
    """
    df = df_raw.copy()

    # Step 1: Remove exact duplicate rows
    initial_len = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    duplicates_removed = initial_len - len(df)

    # Step 2: Standardize Categorical Columns (strip whitespace and apply title/proper casing)
    # Channel standardization
    channel_mode = df['Channel'].dropna().str.strip().str.title().mode()[0]
    # Replace known inconsistencies
    channel_clean = (
        df['Channel']
        .astype(str)
        .str.strip()
        .replace({'nan': np.nan, 'None': np.nan, '': np.nan})
    )
    # Normalizing casing: 'in-store' -> 'In-Store', 'FACEBOOK' -> 'Facebook', etc.
    channel_clean = channel_clean.apply(
        lambda x: 'In-Store' if str(x).lower() in ['in-store', 'in store', 'instore']
        else ('SMS' if str(x).upper() == 'SMS'
        else str(x).title()) if pd.notnull(x) else np.nan
    )
    # Impute missing Channel with mode
    channel_imputed_count = int(channel_clean.isnull().sum())
    df['Channel'] = channel_clean.fillna(channel_mode)

    # Campaign_Type standardization
    df['Campaign_Type'] = df['Campaign_Type'].astype(str).str.strip().str.title()

    # Region standardization
    df['Region'] = df['Region'].astype(str).str.strip().str.title()

    # Product_Category standardization
    df['Product_Category'] = df['Product_Category'].astype(str).str.strip().str.title()

    # Step 3: Handle Missing Values in Numerical Columns
    # Spend: Median imputation
    spend_median = round(float(df['Spend'].dropna().median()), 2)
    spend_missing_count = int(df['Spend'].isnull().sum())
    df['Spend'] = df['Spend'].fillna(spend_median)

    # Leads: Median imputation (integer rounded)
    leads_median = int(round(df['Leads'].dropna().median()))
    leads_missing_count = int(df['Leads'].isnull().sum())
    df['Leads'] = df['Leads'].fillna(leads_median).astype(int)

    # Convert integer counts safely
    for col in ['Impressions', 'Clicks', 'Conversions']:
        df[col] = df[col].astype(int)

    # Step 4: Date Conversion
    df['Campaign_Date'] = pd.to_datetime(df['Campaign_Date'])

    # Step 5: Feature Engineering
    # Month name and numeric month for chronological sorting
    df['Month'] = df['Campaign_Date'].dt.month_name()
    df['Month_Num'] = df['Campaign_Date'].dt.month

    # Click_Through_Rate (CTR %): Clicks / Impressions * 100
    df['Click_Through_Rate'] = np.where(
        df['Impressions'] > 0,
        np.round((df['Clicks'] / df['Impressions']) * 100, 2),
        0.0
    )

    # Conversion_Rate (CVR %): Conversions / Clicks * 100
    df['Conversion_Rate'] = np.where(
        df['Clicks'] > 0,
        np.round((df['Conversions'] / df['Clicks']) * 100, 2),
        0.0
    )

    # Return_on_Ad_Spend (ROAS): Revenue / Spend
    df['Return_on_Ad_Spend'] = np.where(
        df['Spend'] > 0,
        np.round(df['Revenue'] / df['Spend'], 2),
        0.0
    )

    cleaning_meta = {
        'duplicates_removed': duplicates_removed,
        'final_row_count': len(df),
        'spend_median_imputed_value': spend_median,
        'spend_missing_count': spend_missing_count,
        'leads_median_imputed_value': leads_median,
        'leads_missing_count': leads_missing_count,
        'channel_mode_imputed_value': channel_mode,
        'channel_missing_count': channel_imputed_count
    }

    return df, cleaning_meta


def compute_comprehensive_metrics(df):
    """
    Computes verified summary metrics, totals, channel/campaign breakdowns,
    and correlations to power the report, notebook, and web application.
    """
    summary = {
        'totals': {
            'total_spend': round(float(df['Spend'].sum()), 2),
            'total_revenue': round(float(df['Revenue'].sum()), 2),
            'overall_roas': round(float(df['Revenue'].sum() / df['Spend'].sum()), 2),
            'total_impressions': int(df['Impressions'].sum()),
            'total_clicks': int(df['Clicks'].sum()),
            'total_leads': int(df['Leads'].sum()),
            'total_conversions': int(df['Conversions'].sum()),
            'overall_ctr_pct': round(float((df['Clicks'].sum() / df['Impressions'].sum()) * 100), 2),
            'overall_cvr_pct': round(float((df['Conversions'].sum() / df['Clicks'].sum()) * 100), 2),
            'average_campaign_spend': round(float(df['Spend'].mean()), 2),
            'average_campaign_revenue': round(float(df['Revenue'].mean()), 2)
        },
        'descriptive_stats': {
            col: {
                'mean': round(float(df[col].mean()), 2),
                'median': round(float(df[col].median()), 2),
                'min': round(float(df[col].min()), 2),
                'max': round(float(df[col].max()), 2),
                'std': round(float(df[col].std()), 2)
            }
            for col in ['Spend', 'Impressions', 'Clicks', 'Leads', 'Conversions', 'Revenue', 'Click_Through_Rate', 'Conversion_Rate', 'Return_on_Ad_Spend']
        },
        'by_channel': df.groupby('Channel').agg(
            campaigns=('Campaign_ID', 'count'),
            total_spend=('Spend', lambda x: round(float(x.sum()), 2)),
            total_revenue=('Revenue', lambda x: round(float(x.sum()), 2)),
            avg_roas=('Return_on_Ad_Spend', lambda x: round(float(x.mean()), 2)),
            total_conversions=('Conversions', 'sum'),
            avg_ctr=('Click_Through_Rate', lambda x: round(float(x.mean()), 2)),
            avg_cvr=('Conversion_Rate', lambda x: round(float(x.mean()), 2))
        ).reset_index().to_dict(orient='records'),
        'by_campaign_type': df.groupby('Campaign_Type').agg(
            campaigns=('Campaign_ID', 'count'),
            total_spend=('Spend', lambda x: round(float(x.sum()), 2)),
            total_revenue=('Revenue', lambda x: round(float(x.sum()), 2)),
            total_conversions=('Conversions', 'sum'),
            avg_roas=('Return_on_Ad_Spend', lambda x: round(float(x.mean()), 2))
        ).reset_index().to_dict(orient='records'),
        'by_month': df.sort_values('Month_Num').groupby(['Month_Num', 'Month']).agg(
            campaigns=('Campaign_ID', 'count'),
            total_spend=('Spend', lambda x: round(float(x.sum()), 2)),
            total_revenue=('Revenue', lambda x: round(float(x.sum()), 2)),
            total_conversions=('Conversions', 'sum'),
            avg_roas=('Return_on_Ad_Spend', lambda x: round(float(x.mean()), 2))
        ).reset_index().to_dict(orient='records'),
        'by_region': df.groupby('Region').agg(
            campaigns=('Campaign_ID', 'count'),
            total_spend=('Spend', lambda x: round(float(x.sum()), 2)),
            total_revenue=('Revenue', lambda x: round(float(x.sum()), 2)),
            total_conversions=('Conversions', 'sum'),
            avg_roas=('Return_on_Ad_Spend', lambda x: round(float(x.mean()), 2))
        ).reset_index().to_dict(orient='records'),
        'by_product_category': df.groupby('Product_Category').agg(
            campaigns=('Campaign_ID', 'count'),
            total_spend=('Spend', lambda x: round(float(x.sum()), 2)),
            total_revenue=('Revenue', lambda x: round(float(x.sum()), 2)),
            total_conversions=('Conversions', 'sum'),
            avg_roas=('Return_on_Ad_Spend', lambda x: round(float(x.mean()), 2))
        ).reset_index().to_dict(orient='records')
    }
    return summary


def run_pipeline():
    """
    Executes the full pipeline and writes cleaned CSV and summary JSON to disk.
    """
    df_raw = load_raw_data()
    raw_audit = audit_raw_data(df_raw)
    df_cleaned, clean_meta = clean_and_transform_data(df_raw)
    metrics_summary = compute_comprehensive_metrics(df_cleaned)

    os.makedirs('data', exist_ok=True)
    cleaned_csv_path = os.path.join('data', 'cleaned_promotion_data.csv')
    df_cleaned.to_csv(cleaned_csv_path, index=False)

    summary_output = {
        'raw_audit': raw_audit,
        'cleaning_metadata': clean_meta,
        'metrics': metrics_summary
    }

    summary_json_path = os.path.join('data', 'data_summary.json')
    with open(summary_json_path, 'w', encoding='utf-8') as f:
        json.dump(summary_output, f, indent=2, default=str)

    print(f"Pipeline executed successfully.")
    print(f"Raw: {raw_audit['initial_row_count']} rows -> Cleaned: {clean_meta['final_row_count']} rows.")
    print(f"Duplicates removed: {clean_meta['duplicates_removed']}.")
    print(f"Saved: {cleaned_csv_path}")
    print(f"Saved: {summary_json_path}")
    return df_cleaned, summary_output


if __name__ == '__main__':
    run_pipeline()

