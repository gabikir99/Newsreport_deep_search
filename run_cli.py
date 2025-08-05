#!/usr/bin/env python3
"""
CLI entry point for the AI Newsletter Research Tool.
Run this file to use the command-line interface.
"""

import sys
import os
import asyncio
from dotenv import load_dotenv

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.research_pipeline import run_research_pipeline, send_report_email

# Try to import IPython for display functionality
try:
    from IPython.display import display, Markdown
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False


def display_report_summary(report):
    """Display the report summary and follow-up questions"""
    print("\n" + "="*60)
    print("RESEARCH COMPLETE")
    print("="*60)
    print(f"\nSummary: {report.short_summary}")
    print(f"\nFollow-up questions:")
    for i, question in enumerate(report.follow_up_questions, 1):
        print(f"{i}. {question}")


def display_full_report(report):
    """Display the full report using IPython if available, otherwise plain text"""
    print("\n" + "="*60)
    print("FULL REPORT")
    print("="*60)
    if IPYTHON_AVAILABLE:
        display(Markdown(report.markdown_report))
    else:
        print(report.markdown_report)


def get_user_input(prompt: str) -> str:
    """Get user input with error handling"""
    try:
        return input(prompt).lower().strip()
    except (EOFError, KeyboardInterrupt):
        return ""


async def main():
    """Main function that orchestrates the research pipeline"""
    try:
        # Load environment variables
        load_dotenv(override=True)
        
        # Get the research query from user
        query = input("Enter your research query: ")
        
        if not query.strip():
            print("No query provided. Exiting...")
            return
        
        print(f"\nStarting research for: '{query}'\n")
        
        # Run the research pipeline
        report = await run_research_pipeline(query)
        
        # Display the report summary
        display_report_summary(report)
        
        # Ask user if they want to send the email
        print("\n" + "-"*60)
        send_choice = get_user_input("Would you like to send this report via email? (y/n): ")
        
        if send_choice in ['y', 'yes']:
            await send_report_email(report)
            print("✅ Report has been sent via email!")
        else:
            print("📄 Report generated but not sent via email.")
            
        # Option to display the full report
        display_choice = get_user_input("Would you like to display the full report here? (y/n): ")
        if display_choice in ['y', 'yes']:
            display_full_report(report)
                
    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user.")
    except Exception as e:
        print(f"\nError occurred: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())