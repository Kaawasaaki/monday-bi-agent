# Monday.com Business Intelligence Agent

## Project Overview
This project is a specialized Business Intelligence (BI) Agent developed for the Skylark Drones technical assignment. It provides a conversational interface that allows founders and executives to query complex, multi-source business data stored in Monday.com boards.

The agent focuses on bridging the gap between high-level business questions and "messy" operational data, providing narrative insights rather than simple data dumps.

## Core Features

### 1. Data Resilience Layer
The agent is designed to handle real-world data inconsistencies gracefully:
- **Automatic Type Coercion**: Handles currency symbols (INR, Rs.), commas, and accidental string-to-number concatenations.
- **Error Handling**: Detects and neutralizes common spreadsheet errors such as `#VALUE!` or missing records without crashing the analysis.
- **Fuzzy Column Mapping**: Employs heuristic matching to identify relevant columns (e.g., "Revenue" vs "Masked Deal Value") even if board schemas are modified.

### 2. Cross-Board Intelligence
The system performs relational joins between disparate data sources:
- **Sales vs. Operations**: Maps the 'Deals Pipeline' to the 'Work Order Tracker' using 'Item Name' as a primary key.
- **Bottleneck Identification**: Specifically identifies "Won" deals that have not yet transitioned into "Started" execution phases.

### 3. Professional BI Console
- **Executive Metrics**: High-level summary of Total Pipeline Value, Active Orders, and Sector Performance visible upon data synchronization.
- **Conversational Reasoning**: Uses a ReAct (Reasoning and Acting) framework to determine which data tools to call based on user intent.
- **Audit Transparency**: Provides expandable raw data views for manual verification of the agent's cleaning process.

## Technical Stack
- **Language**: Python 3.10+
- **Frontend**: Streamlit (Management Console)
- **Agent Framework**: LangChain (Modular Agent Architecture)
- **LLM Engine**: Groq (Llama 3.3 70B) for high-speed, low-latency reasoning.
- **Data Engine**: Pandas & NumPy for robust data cleaning and transformations.
- **Integration**: Monday.com GraphQL API v2 (2024-01).

## Architecture Overview
```text
monday-bi-agent/
├── app.py                  # Main BI Console and UI Logic
├── agent/
│   ├── agent_factory.py    # LLM Initialization and Chain Construction
│   ├── tools.py            # Specialized BI Data Tools
│   └── prompts.py          # Founder-Level Persona and Instructions
├── integrations/
│   └── monday_clients.py   # Monday.com GraphQL API Client
├── utils/
│   └── data_cleaner.py     # Resilience Layer (Regex-based Normalization)
└── requirements.txt        # System Dependencies
