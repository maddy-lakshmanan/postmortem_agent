from dotenv import load_dotenv
load_dotenv()

import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek.chat_models import ChatDeepSeek
from sample_incident import incident_data

assert os.getenv("DEEPSEEK_API_KEY"), "Missing DEEPSEEK_API_KEY env var"

llm = ChatDeepSeek(model="deepseek-chat", temperature=0.0)
parser = StrOutputParser()

# State Definition
class AgentState(TypedDict):
    input_data: dict
    postmortem: Annotated[str, lambda x: x or ""]
    action_items: Annotated[str, lambda x: x or ""]
    remediation_tracker: Annotated[str, lambda x: x or ""]

# Prompts (same as before)
postmortem_prompt = PromptTemplate.from_template("""...""")  # Your template
action_items_prompt = PromptTemplate.from_template("""...""")  # Your template
remediation_prompt = PromptTemplate.from_template("""...""")  # Your template

# Nodes
def generate_postmortem(state: AgentState):
    chain = postmortem_prompt | llm | parser
    return {"postmortem": chain.invoke(state["input_data"])}

def extract_action_items(state: AgentState):
    chain = action_items_prompt | llm | parser
    return {"action_items": chain.invoke({"postmortem": state["postmortem"]})}

def create_remediation_tracker(state: AgentState):
    chain = remediation_prompt | llm | parser
    return {"remediation_tracker": chain.invoke({"action_items": state["action_items"]})}

# Graph Construction
workflow = StateGraph(AgentState)

# Add nodes (parallel capable)
workflow.add_node("generate_postmortem", generate_postmortem)
workflow.add_node("extract_actions", extract_action_items)
workflow.add_node("create_tracker", create_remediation_tracker)

# Define edges
workflow.add_edge("generate_postmortem", "extract_actions")
workflow.add_edge("extract_actions", "create_tracker")
workflow.add_edge("create_tracker", END)

# Compile
agent = workflow.compile()

# Execution
result = agent.invoke({"input_data": incident_data})

# Output
print("\n📘 Postmortem:\n", result["postmortem"])
print("\n✅ Action Items:\n", result["action_items"])
print("\n📊 Remediation Tracker:\n", result["remediation_tracker"])