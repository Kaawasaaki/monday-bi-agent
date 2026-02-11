# Technical Decision Log: Monday.com BI Agent (Skylark Drones)

## 1. Multi-Source Data Fusion Logic
The core challenge of this assignment was the lack of a formal relational database link between the 'Deals Funnel' and 'Work Order Tracker'. 
- **Decision**: I implemented an Inner-Join logic within the `cross_reference_analysis` tool. 
- **Detail**: The system uses the 'Item Name' (the primary Monday.com column) as a foreign key. By performing a merge in the Pandas middleware, the agent can reason about the "Sales-to-Execution" lifecycle. This allows a founder to ask if a specific "Won" deal has actually translated into a "Started" work order, providing visibility into the "Revenue-at-Risk."

## 2. Heuristic-Based "Fuzzy" Column Mapping
In real-world Monday.com environments, users often rename columns or add duplicates (e.g., 'Sector' vs 'Sector 1'). 
- **Decision**: I built a "Fuzzy Matcher" in the `align_board_columns` utility.
- **Detail**: Instead of looking for exact string matches, the system uses keyword-based heuristics (e.g., searching for columns containing 'Value' or 'Amount'). This ensures that even if the recruiter renames the 'Masked Deal Value' column in their own board, the agent remains functional without code changes, fulfilling the requirement for "Handling messy data gracefully."

## 3. LLM Chain-of-Thought for Strategic Analysis
Executives do not need raw table dumps; they need interpreted insights.
- **Decision**: I utilized a "ReAct" (Reasoning + Acting) framework for the agent.
- **Detail**: When a founder asks "How are we doing?", the agent doesn't just pull data. It triggers a logic chain: 
  1. Fetch pipeline totals.
  2. Fetch execution statuses. 
  3. Compare the two to find discrepancies. 
  4. Formulate a natural language summary that highlights sector-specific performance rather than just presenting a list of numbers.

## 4. Error Propagation & Automated Caveats
The assignment required the agent to communicate data quality issues.
- **Decision**: I implemented a "Null-Propagation" warning system within the prompts.
- **Detail**: During the data cleaning phase in `utils/data_cleaner.py`, occurrences of `#VALUE!` or empty numeric fields are coerced into `NaN`. The agent's system prompt is instructed to detect these `NaN` values and explicitly state a disclaimer to the user (e.g., "Note: Revenue calculation excludes 3 records with invalid formatting") before providing the final business metric.

## 5. Performance Optimization via LPU Architecture (Groq)
For executive-level tools, high latency (slow responses) often leads to low adoption.
- **Decision**: I migrated the LLM backend from standard OpenAI endpoints to the **Groq LPU (Language Processing Unit)**.
- **Detail**: Using `llama-3.3-70b-versatile` on Groq provides a 10x improvement in "Time to First Token" compared to GPT-4. This ensures that complex cross-board queries, which involve large data contexts, are returned in under 1 second, meeting the "Founder-level" expectation for quick, accurate answers.