from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub
from .tools import get_pipeline_summary, get_execution_metrics, cross_reference_analysis
from .prompts import SYSTEM_PROMPT

def create_bi_agent(api_key):
    """
    Initializes the BI Agent using the latest 0.3.x Tool Calling standard.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0, 
        groq_api_key=api_key
    )
    
    tools = [
        get_pipeline_summary, 
        get_execution_metrics, 
        cross_reference_analysis
    ]
    
    # This pulls the official tool-calling prompt
    prompt = hub.pull("hwchase17/openai-tools-agent")
    
    # This ensures your "Founder" persona is active
    prompt.messages[0].prompt.template = SYSTEM_PROMPT
    
    # This is the modern standard for 0.3.x
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )