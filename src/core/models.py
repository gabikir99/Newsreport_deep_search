from pydantic import BaseModel, Field
from typing import Dict, List

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to be used to find the information.")

class WebSearchPlan(BaseModel):
    searches: List[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: List[str] = Field(description="Suggested topics to research further")