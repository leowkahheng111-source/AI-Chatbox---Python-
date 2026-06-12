"""
============================================================================
CHAT PROMPTS
============================================================================
Purpose: Store prompts and templates for AI chat integration
Usage: Used by chat_service when AI APIs are integrated
Expansion: Add more sophisticated prompts for different scenarios
============================================================================
"""

# System prompts for AI integration (OpenAI, Gemini)
SYSTEM_PROMPT = """You are Mini AI Chatbox, a helpful and friendly assistant specialized in:
- Mathematical calculations and problem-solving
- SQL database queries and best practices
- Power BI DAX formulas and data modeling
- SPSS statistical analysis and interpretation

Be concise, accurate, and educational. Help users learn while solving their problems."""

# User prompt templates
CHAT_PROMPT_TEMPLATE = """User question: {user_input}

Please provide a helpful, friendly response. If the question is about calculations, SQL, DAX, or statistics, provide specific guidance."""

# TODO: Add more prompts for different AI providers
# TODO: Add few-shot examples for better responses
# TODO: Add domain-specific prompts for each module
