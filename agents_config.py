from agents import Agent, WebSearchTool, ModelSettings
from models import WebSearchPlan, ReportData
from email_service import send_email

# Configuration
HOW_MANY_SEARCHES = 5

# Instructions for different agents
INSTRUCTIONS_SEARCH = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

INSTRUCTIONS_PLANNER = (
    f"You are a helpful research assistant. Given a query, come up with a set of web searches "
    f"to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."
)

INSTRUCTIONS_EMAIL = (
    "You are able to send a nicely formatted HTML email based on a detailed report. "
    "You will be provided with a detailed report. You should use your tool to send one email, providing the "
    "report converted into clean, well presented HTML with an appropriate subject line."
)

INSTRUCTIONS_WRITER = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)

# Agent configurations
search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS_SEARCH,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS_PLANNER,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS_EMAIL,
    tools=[send_email],
    model="gpt-4o-mini",
)

writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS_WRITER,
    model="gpt-4o-mini",
    output_type=ReportData,
)