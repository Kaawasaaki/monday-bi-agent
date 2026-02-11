import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from integrations.monday_clients import MondayClient
from utils.data_cleaner import clean_business_data, align_board_columns
from agent.agent_factory import create_bi_agent

load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Business Intelligence Console | Skylark Drones",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Professional Look ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        border: 1px solid #e1e4e8; 
        padding: 15px; 
        border-radius: 5px; 
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "deals_df" not in st.session_state:
    st.session_state.deals_df = None
if "orders_df" not in st.session_state:
    st.session_state.orders_df = None

# --- Sidebar: System Configuration ---
with st.sidebar:
    st.title("System Control")
    st.markdown("---")
    
    with st.expander("Authentication Settings", expanded=True):
        m_key = st.text_input("Monday API Key", type="password", value=os.getenv("MONDAY_API_KEY", ""))
        o_key = st.text_input("Groq API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    with st.expander("Data Source Mapping", expanded=True):
        d_id = st.text_input("Deals Board ID", value=os.getenv("DEALS_BOARD_ID", ""))
        o_id = st.text_input("Orders Board ID", value=os.getenv("ORDERS_BOARD_ID", ""))
    
    st.markdown("---")
    
    if st.button("Synchronize Data Sources"):
        if not m_key or not d_id or not o_id:
            st.error("Authentication credentials incomplete.")
        else:
            with st.spinner("Processing remote data..."):
                client = MondayClient(m_key)
                df_deals = client.fetch_board(d_id)
                df_orders = client.fetch_board(o_id)
                
                if not df_deals.empty and not df_orders.empty:
                    df_deals = clean_business_data(df_deals)
                    df_orders = clean_business_data(df_orders)
                    df_deals, df_orders = align_board_columns(df_deals, df_orders)
                    
                    st.session_state.deals_df = df_deals
                    st.session_state.orders_df = df_orders
                else:
                    st.sidebar.error("Synchronization failed. Validate Board IDs.")

# --- Main Console Layout ---
st.title("Business Intelligence Management Console")
st.caption("Skylark Drones Operations and Sales Pipeline Analysis")
st.markdown("---")

if st.session_state.deals_df is not None:
    # --- Executive Dashboard Header ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Force conversion to numeric to prevent string concatenation errors
    deals_rev = pd.to_numeric(st.session_state.deals_df['revenue'], errors='coerce').fillna(0)
    orders_df = st.session_state.orders_df
    
    total_pipeline = deals_rev.sum()
    active_orders = len(orders_df)
    
    # Filter for Mining sector and ensure it is numeric
    mining_mask = st.session_state.deals_df['sector'].str.contains('Mining', na=False)
    mining_revenue = pd.to_numeric(st.session_state.deals_df[mining_mask]['revenue'], errors='coerce').fillna(0).sum()
    
    with col1:
        st.metric("Total Pipeline Value", f"INR {float(total_pipeline):,.2f}")
    with col2:
        st.metric("Active Work Orders", active_orders)
    with col3:
        st.metric("Mining Sector Value", f"INR {float(mining_revenue):,.2f}")
    with col4:
        # Check system health based on data presence
        status = "Operational" if not st.session_state.deals_df.empty else "No Data"
        st.metric("System Status", status)
    st.markdown("### Conversational Analysis")
    
    # --- Chat History Container ---
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # --- Chat Input ---
    if prompt := st.chat_input("Enter business query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not o_key:
                st.error("AI Authentication Key Missing.")
            else:
                try:
                    agent_executor = create_bi_agent(o_key)
                    with st.spinner("Generating insights..."):
                        response = agent_executor.invoke({"input": prompt})
                        answer = response["output"]
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Intelligence Layer Error: {str(e)}")

    
    with st.expander("Audit Raw Data Tables"):
        tab1, tab2 = st.tabs(["Pipeline Data", "Execution Data"])
        with tab1:
            st.dataframe(st.session_state.deals_df, use_container_width=True)
        with tab2:
            st.dataframe(st.session_state.orders_df, use_container_width=True)

else:
    
    st.empty()
    st.warning("System awaiting data synchronization. Please utilize the control panel to initialize the connection.")
    
    st.markdown("""
    #### Integration Requirements
    - **Monday.com**: Read-only access to Sales and Operations boards.
    - **Groq/OpenAI**: Active API key for natural language processing.
    - **Data Resilience**: Automated handling of null values and inconsistent formatting.
    """)