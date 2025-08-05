"""
Custom agent system to replace the 'agents' dependency.
Uses OpenAI API directly with web search capabilities.
"""

import os
import json
import asyncio
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from openai import AsyncOpenAI
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class AgentResult:
    """Result from an agent execution"""
    final_output: Any
    raw_response: str


class WebSearchTool:
    """Simple web search tool using DuckDuckGo"""
    
    def __init__(self, search_context_size: str = "low"):
        self.context_size = search_context_size
        self.max_results = 5 if search_context_size == "low" else 10
    
    async def search(self, query: str) -> str:
        """Perform web search and return summarized results"""
        try:
            # Use DuckDuckGo Instant Answer API (no API key required)
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Make the search request
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML response
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract search results
            results = []
            result_links = soup.find_all('a', class_='result__a')[:self.max_results]
            
            for link in result_links:
                title = link.get_text(strip=True)
                url = link.get('href', '')
                
                # Try to get snippet from the result
                result_div = link.find_parent('div', class_='result')
                snippet = ""
                if result_div:
                    snippet_elem = result_div.find('a', class_='result__snippet')
                    if snippet_elem:
                        snippet = snippet_elem.get_text(strip=True)
                
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet
                })
            
            # Format results for the agent
            if not results:
                return f"No search results found for query: {query}"
            
            formatted_results = f"Search results for '{query}':\n\n"
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. {result['title']}\n"
                if result['snippet']:
                    formatted_results += f"   {result['snippet']}\n"
                formatted_results += f"   URL: {result['url']}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Search error for query '{query}': {str(e)}"


class Agent:
    """Simple agent that uses OpenAI for reasoning and optional tools"""
    
    def __init__(
        self, 
        name: str, 
        instructions: str, 
        model: str = "gpt-4o-mini",
        tools: Optional[List] = None,
        output_type: Optional[type] = None,
        model_settings: Optional[Dict] = None
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []
        self.output_type = output_type
        self.model_settings = model_settings or {}
        
        # Get API key and validate
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file or environment variables."
            )
        
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def run(self, user_input: str) -> AgentResult:
        """Execute the agent with the given input"""
        
        # Prepare the system message
        system_message = self.instructions
        
        # If we have tools, use them first
        tool_results = ""
        email_tool = None
        if self.tools:
            for tool in self.tools:
                if isinstance(tool, WebSearchTool):
                    # Extract search query from user input
                    search_result = await tool.search(user_input)
                    tool_results += f"\nSearch Results:\n{search_result}\n"
                elif callable(tool):  # For email tool
                    email_tool = tool
                    tool_results += "\nEmail tool is available for sending emails.\n"
        
        # Combine input with tool results
        full_input = user_input
        if tool_results:
            full_input += f"\n\nAdditional Context:\n{tool_results}"
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": full_input}
        ]
        
        # Handle structured output if specified
        if self.output_type:
            # Add JSON schema instruction
            if hasattr(self.output_type, 'model_json_schema'):
                schema = self.output_type.model_json_schema()
                schema_instruction = f"\n\nRespond with valid JSON that matches this schema:\n{json.dumps(schema, indent=2)}"
                messages[0]["content"] += schema_instruction
        
        try:
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=2000
            )
            
            raw_response = response.choices[0].message.content
            
            # If this is an email agent with an email tool, execute the email sending
            if email_tool and "email" in self.name.lower():
                try:
                    # Extract subject and HTML content from the response
                    # Look for HTML content in the response
                    html_match = re.search(r'<html.*?</html>', raw_response, re.DOTALL | re.IGNORECASE)
                    if html_match:
                        html_content = html_match.group()
                        # Try to extract subject from HTML title or create a default
                        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
                        if title_match:
                            subject = title_match.group(1)
                        else:
                            subject = "AI Research Report"
                        
                        print(f"[EMAIL AGENT] Sending email with subject: {subject}")
                        print(f"[EMAIL AGENT] HTML content length: {len(html_content)} characters")
                        
                        # Call the email tool
                        email_result = email_tool(subject, html_content)
                        print(f"[EMAIL AGENT] Email send result: {email_result}")
                        
                        # Update response to include send result
                        raw_response += f"\n\nEmail sent: {email_result}"
                    else:
                        print("[EMAIL AGENT] No HTML content found in response, not sending email")
                except Exception as e:
                    print(f"[EMAIL AGENT] Error sending email: {e}")
                    raw_response += f"\n\nEmail sending failed: {str(e)}"
            
            # Parse output based on type
            if self.output_type:
                try:
                    # Try to parse as JSON for Pydantic models
                    if raw_response.strip().startswith('{'):
                        json_data = json.loads(raw_response)
                        final_output = self.output_type(**json_data)
                    else:
                        # If not JSON, try to extract JSON from the response
                        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
                        if json_match:
                            json_data = json.loads(json_match.group())
                            final_output = self.output_type(**json_data)
                        else:
                            # Fallback: return raw response
                            final_output = raw_response
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"Warning: Could not parse structured output for {self.name}: {e}")
                    final_output = raw_response
            else:
                final_output = raw_response
            
            return AgentResult(final_output=final_output, raw_response=raw_response)
            
        except Exception as e:
            error_msg = f"Error in agent {self.name}: {str(e)}"
            return AgentResult(final_output=error_msg, raw_response=error_msg)


class Runner:
    """Simple runner to execute agents"""
    
    @staticmethod
    async def run(agent: Agent, user_input: str) -> AgentResult:
        """Run an agent with the given input"""
        return await agent.run(user_input)


def function_tool(func):
    """Decorator to mark functions as tools (for compatibility)"""
    return func