import asyncio
from typing import List
from src.agents.custom_agents import Runner
from src.core.models import WebSearchPlan, WebSearchItem, ReportData
from src.config.agents_config import search_agent, planner_agent, writer_agent, email_agent


async def plan_searches(query: str) -> WebSearchPlan:
    """Use the planner_agent to plan which searches to run for the query"""
    print("Planning searches...")
    result = await Runner.run(planner_agent, f"Query: {query}")
    print(f"Will perform {len(result.final_output.searches)} searches")
    return result.final_output


async def perform_searches(search_plan: WebSearchPlan) -> List[str]:
    """Call search() for each item in the search plan"""
    print("Searching...")
    tasks = [asyncio.create_task(search(item)) for item in search_plan.searches]
    results = await asyncio.gather(*tasks)
    print("Finished searching")
    return results


async def search(item: WebSearchItem) -> str:
    """Use the search agent to run a web search for each item in the search plan"""
    input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
    result = await Runner.run(search_agent, input_text)
    return result.final_output


async def write_report(query: str, search_results: List[str]) -> ReportData:
    """Use the writer agent to write a report based on the search results"""
    print("Thinking about report...")
    input_text = f"Original query: {query}\nSummarized search results: {search_results}"
    result = await Runner.run(writer_agent, input_text)
    print("Finished writing report")
    return result.final_output


async def send_report_email(report: ReportData) -> ReportData:
    """Use the email agent to send an email with the report"""
    try:
        print("[PIPELINE] Starting email generation and sending...")
        print(f"[PIPELINE] Report length: {len(report.markdown_report)} characters")
        
        # The email agent will process the markdown report and send it
        result = await Runner.run(email_agent, report.markdown_report)
        
        print(f"[PIPELINE] Email agent result: {result.final_output}")
        print("[PIPELINE] Email process completed")
        
        return report
        
    except Exception as e:
        print(f"[PIPELINE ERROR] Failed to send email: {str(e)}")
        import traceback
        traceback.print_exc()
        # Don't fail the whole pipeline, just log the error
        return report


async def run_research_pipeline(query: str) -> ReportData:
    """Main research pipeline that orchestrates all steps"""
    # Step 1: Plan the searches
    search_plan = await plan_searches(query)
    
    # Step 2: Perform all searches
    search_results = await perform_searches(search_plan)
    
    # Step 3: Write the report
    report = await write_report(query, search_results)
    
    return report