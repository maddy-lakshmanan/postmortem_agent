from dotenv import load_dotenv
load_dotenv()

import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel  # Added import
from langchain_deepseek.chat_models import ChatDeepSeek
from sample_incident import incident_data

assert os.getenv("DEEPSEEK_API_KEY"), "Missing DEEPSEEK_API_KEY env var"

llm = ChatDeepSeek(model="deepseek-chat", temperature=0.0)
parser = StrOutputParser()

# Prompts (unchanged)
postmortem_prompt = PromptTemplate.from_template("""
Generate a clear, structured postmortem for the incident below:

Incident ID: {incident_id}
Title: {title}
Start Time: {start_time}
End Time: {end_time}
Impact: {impact}
Detection: {detection}
Resolution: {resolution}
Root Cause: {root_cause}
Slack Summary:
{slack_summary}

Structure:
- Overview
- Timeline
- Root Cause Analysis
- Resolution Steps
- Lessons Learned
- Impact Assessment
""")

action_items_prompt = PromptTemplate.from_template("""
From the following postmortem, extract clear action items with owner suggestions and proposed due dates (within 1-2 weeks):

{postmortem}
""")

remediation_tracker_prompt = PromptTemplate.from_template("""
Convert the following action items into a remediation tracker table (Markdown format) with columns: Task, Owner, Due Date, Status.

{action_items}
""")

# Chains
generate_postmortem = postmortem_prompt | llm | parser
extract_action_items = action_items_prompt | llm | parser
generate_tracker = remediation_tracker_prompt | llm | parser

# Working implementation
postmortem_agent = (
    RunnablePassthrough.assign(postmortem=generate_postmortem)
    .assign(action_items=lambda x: extract_action_items.invoke(x["postmortem"]))
    .assign(remediation_tracker=lambda x: generate_tracker.invoke(x["action_items"]))
)

# Run
result = postmortem_agent.invoke(incident_data)

# Output
print("\n📘 Postmortem:\n", result['postmortem'])
print("\n✅ Action Items:\n", result['action_items'])
print("\n📊 Remediation Tracker:\n", result['remediation_tracker'])