#!/usr/bin/env python3
"""
Environment checker for the AI Newsletter Research Tool.
Run this to verify your .env file is set up correctly.
"""

import os
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    print("🔍 Checking environment setup...\n")
    
    # Load environment variables
    load_dotenv()
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for AI agents',
        'SENDGRID_API_KEY': 'SendGrid API key for email sending'
    }
    
    all_good = True
    
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        
        if value:
            # Show first 10 characters and mask the rest
            masked_value = value[:10] + '...' if len(value) > 10 else value
            print(f"✅ {var_name}: {masked_value} ({description})")
        else:
            print(f"❌ {var_name}: Not set ({description})")
            all_good = False
    
    print("\n" + "="*50)
    
    if all_good:
        print("🎉 All environment variables are set correctly!")
        print("You can now run:")
        print("  • uv run python run_web.py (web interface)")
        print("  • uv run python run_cli.py (command line)")
    else:
        print("⚠️  Missing environment variables!")
        print("\nPlease create a .env file in the project root with:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("SENDGRID_API_KEY=your_sendgrid_api_key_here")
        print("\nGet your keys from:")
        print("• OpenAI: https://platform.openai.com/api-keys")
        print("• SendGrid: https://app.sendgrid.com/settings/api_keys")

if __name__ == "__main__":
    check_environment()