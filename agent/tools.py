import pandas as pd
import streamlit as st
from langchain.tools import tool

def get_context():
    """
    Retrieves the synced dataframes from the application session state.
    """
    return st.session_state.get('deals_df'), st.session_state.get('orders_df')

@tool
def get_pipeline_summary(query: str):
    """
    Answers questions about sales pipeline, deal stages, and total potential revenue.
    """
    deals, _ = get_context()
    if deals is None or deals.empty:
        return "No deal data synced."
    
    summary = {
        "total_deals": len(deals),
        "total_revenue": deals['revenue'].sum(),
        "sector_breakdown": deals.groupby('sector')['revenue'].sum().to_dict(),
        "stage_distribution": deals['Deal Stage'].value_counts().to_dict()
    }
    return f"Pipeline Summary: {summary}"

@tool
def get_execution_metrics(query: str):
    """
    Answers questions about project progress, work order status, and operational efficiency.
    """
    _, orders = get_context()
    if orders is None or orders.empty:
        return "No work order data synced."
    
    metrics = {
        "active_projects": len(orders),
        "status_count": orders['Execution Status'].value_counts().to_dict(),
        "sector_progress": orders.groupby('sector')['Execution Status'].value_counts().unstack().fillna(0).to_dict()
    }
    return f"Operational Metrics: {metrics}"

@tool
def cross_reference_analysis(query: str):
    """
    Links Sales Deals with Work Orders to find bottlenecks or performance gaps.
    Useful for questions like 'Which won deals haven't started execution yet?'
    """
    deals, orders = get_context()
    if deals is None or orders is None:
        return "Data from both boards is required for this analysis."
    
    merged = pd.merge(deals, orders, on='deal_id', how='inner', suffixes=('_deal', '_order'))
    
    if merged.empty:
        return "No matching records found between Deals and Work Orders using 'Item Name'."
    
    analysis = {
        "matched_records": len(merged),
        "revenue_at_risk": merged[merged['Execution Status'] == 'Not Started']['revenue_deal'].sum()
    }
    return f"Cross-Board Analysis: {analysis}"