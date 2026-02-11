import pandas as pd
import numpy as np

def clean_business_data(df):
    if df.empty:
        return df
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # Identify numeric columns
    numeric_keywords = ['Amount', 'Value', 'Rupees', 'Quantity', 'Billed', 'Collected']
    for col in df.columns:
        if any(key in col for key in numeric_keywords):
            # STRICTOR CLEANING: Remove everything except digits and dots
            df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)

    date_keywords = ['Date', 'Month', 'Close', 'Start', 'End']
    for col in df.columns:
        if any(key in col for key in date_keywords):
            df[col] = pd.to_datetime(df[col], errors='coerce')

    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].fillna('Not Provided')
    return df

def align_board_columns(deals_df, orders_df):
    def find_col(df, keyword):
        for col in df.columns:
            if keyword.lower() in col.lower():
                return col
        return None

    d_sec = find_col(deals_df, 'Sector')
    d_rev = find_col(deals_df, 'Value')
    deals_df = deals_df.rename(columns={'item_name': 'deal_id', d_sec: 'sector', d_rev: 'revenue'})

    o_sec = find_col(orders_df, 'Sector')
    o_rev = find_col(orders_df, 'Amount')
    orders_df = orders_df.rename(columns={'item_name': 'deal_id', o_sec: 'sector', o_rev: 'revenue'})
    
    return deals_df, orders_df