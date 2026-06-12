"""
============================================================================
CHAT SERVICE - General Conversation Module
============================================================================
Purpose: Handle general conversation and questions
Usage: Responds when no specific skill is detected
Expansion: Integrate with OpenAI/Gemini for intelligent responses
============================================================================
"""

# Standard Library Imports
import logging
import random
import os
from typing import Dict, Any, Optional, List

# Third-Party Imports
try:
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Internal Project Imports
from backend.exception_handler import handle_errors
from config.settings import Settings


# Configure logger
logger = logging.getLogger(__name__)


class ChatService:
    """
    General conversation module for the chatbot.
    
    Why this exists:
        - Default fallback when no specific skill matches
        - Handles greetings, help requests, general questions
        - Provides friendly, conversational interface
    
    Current Implementation: Rule-based responses
    Future: Integrate AI (OpenAI GPT, Google Gemini)
    
    Capabilities:
        - Greetings (hello, hi, hey)
        - Help requests (what can you do?)
        - Farewells (goodbye, bye)
        - General questions
        - Friendly fallback responses
    """
    
    def __init__(self):
        """Initialize chat service with response patterns and AI model."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize AI model if available
        self.ai_model = None
        self.use_ai = False
        
        if AI_AVAILABLE:
            try:
                # Get API key from environment variable
                api_key = os.getenv("GOOGLE_API_KEY") or Settings.GOOGLE_API_KEY
                
                if api_key:
                    self.logger.info("Initializing Google Gemini AI...")
                    genai.configure(api_key=api_key)
                    self.ai_model = genai.GenerativeModel('gemini-pro')
                    self.use_ai = True
                    self.logger.info("✅ Google Gemini AI ready!")
                else:
                    self.logger.warning("No Google API key found. Using rule-based responses.")
                    self.logger.warning("Add GOOGLE_API_KEY to your .env file to enable AI")
                    self.use_ai = False
            except Exception as e:
                self.logger.warning(f"Failed to initialize Gemini AI: {e}. Using rule-based responses.")
                self.use_ai = False
        else:
            self.logger.warning("google-generativeai library not installed. Using rule-based responses.")
        
        # Response patterns for different intents (fallback)
        self.greetings = [
            "Hello! How can I help you today?",
            "Hi there! What would you like to know?",
            "Hey! I'm here to assist you.",
            "Greetings! What can I do for you?",
        ]
        
        self.help_responses = [
            """I can help you with:
            
🧮 **Calculator**: Math operations and calculations
📊 **SQL Helper**: Database queries and SQL syntax
📈 **Power BI DAX**: DAX formulas and measures
📉 **SPSS**: Statistical analysis guidance
💬 **General Chat**: Conversations and questions

Just ask me anything!""",
        ]
        
        self.farewells = [
            "Goodbye! Feel free to come back anytime!",
            "See you later! Have a great day!",
            "Bye! Let me know if you need anything else.",
        ]
        
        self.fallback_responses = [
            "I'm here to chat! Feel free to ask me anything about calculations, SQL, Power BI DAX, or SPSS.",
            "I'm not sure I understand. Could you rephrase that? Or try asking about calculations, SQL queries, DAX formulas, or statistics.",
            "Interesting question! I can help with math calculations, SQL queries, Power BI DAX, and SPSS analysis. What would you like to explore?",
        ]
        
        self.logger.info("ChatService initialized")
    
    @handle_errors("chat_service_process")
    def process(
        self,
        user_input: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Process general conversation input.
        
        Args:
            user_input: User's message
            session_id: Optional session ID for context
            
        Returns:
            Response string
            
        Logic:
            1. Normalize input
            2. Check for specific patterns (greetings, help, etc.)
            3. Return appropriate response
            4. Fallback to generic response if no match
        """
        if not user_input:
            return "Please provide a message."
        
        # Normalize input
        normalized_input = user_input.lower().strip()
        
        self.logger.debug(f"Processing chat input: {normalized_input[:50]}...")
        
        # Check for greetings
        if self._is_greeting(normalized_input):
            return self._get_random_response(self.greetings)
        
        # Check for help requests
        if self._is_help_request(normalized_input):
            return self._get_random_response(self.help_responses)
        
        # Check for farewells
        if self._is_farewell(normalized_input):
            return self._get_random_response(self.farewells)
        
        # Check for "who are you" questions
        if self._is_about_bot(normalized_input):
            return self._get_bot_description()
        
        # Try AI response if available
        if self.use_ai and self.ai_model:
            try:
                ai_response = self._get_ai_response(user_input)
                if ai_response:
                    return ai_response
            except Exception as e:
                self.logger.error(f"AI response failed: {e}")
        
        # Default fallback
        return self._get_random_response(self.fallback_responses)
    
    def _is_greeting(self, text: str) -> bool:
        """
        Check if input is a greeting.
        
        Args:
            text: Normalized input text
            
        Returns:
            True if greeting detected
        """
        greeting_keywords = [
            "hello", "hi", "hey", "greetings", "good morning",
            "good afternoon", "good evening", "howdy", "hiya"
        ]
        
        return any(keyword in text for keyword in greeting_keywords)
    
    def _is_help_request(self, text: str) -> bool:
        """
        Check if input is a help request.
        
        Args:
            text: Normalized input text
            
        Returns:
            True if help request detected
        """
        help_keywords = [
            "help", "what can you do", "capabilities", "features",
            "how can you help", "what do you do", "skills",
            "what are you", "functions"
        ]
        
        return any(keyword in text for keyword in help_keywords)
    
    def _is_farewell(self, text: str) -> bool:
        """
        Check if input is a farewell.
        
        Args:
            text: Normalized input text
            
        Returns:
            True if farewell detected
        """
        farewell_keywords = [
            "bye", "goodbye", "see you", "farewell", "talk later",
            "catch you later", "take care", "until next time"
        ]
        
        return any(keyword in text for keyword in farewell_keywords)
    
    def _is_about_bot(self, text: str) -> bool:
        """
        Check if user is asking about the bot.
        
        Args:
            text: Normalized input text
            
        Returns:
            True if asking about bot
        """
        about_keywords = [
            "who are you", "what are you", "tell me about yourself",
            "who made you", "what is your name", "introduce yourself"
        ]
        
        return any(keyword in text for keyword in about_keywords)
    
    def _get_bot_description(self) -> str:
        """
        Return bot description.
        
        Returns:
            Description of the chatbot
        """
        return """I'm Mini AI Chatbox, your intelligent assistant for:

🧮 **Mathematical Calculations** - Solve expressions and equations
🗃️ **SQL Database Help** - Learn SQL syntax and best practices  
📊 **Power BI DAX** - Master DAX formulas and measures
📈 **SPSS Statistics** - Understand statistical analysis

I'm built with clean architecture and designed to help students and professionals with data-related tasks!"""
    
    def _get_random_response(self, responses: List[str]) -> str:
        """
        Get a random response from list.
        
        Args:
            responses: List of possible responses
            
        Returns:
            Random response string
            
        Why: Makes conversation feel more natural and less robotic
        """
        return random.choice(responses)
    
    def _get_ai_response(self, user_input: str) -> Optional[str]:
        """
        Get AI-generated response using Google Gemini.
        
        Args:
            user_input: User's message
            
        Returns:
            AI-generated response or None if failed
            
        Why: Provides intelligent, context-aware responses using Google's Gemini AI
        """
        try:
            # Create context-aware prompt
            prompt = f"""You are Mini AI Chatbox, a helpful assistant specializing in:
- Mathematical calculations
- SQL database queries
- Power BI DAX formulas
- SPSS statistical analysis
- General conversation

User question: {user_input}

Provide a helpful, concise response:"""
            
            # Generate response with Gemini
            response = self.ai_model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Gemini AI error: {e}")
            return None


# TODO: Future enhancements
# - Add conversation history/context
# - Implement sentiment analysis
# - Add personality customization
# - Support multi-turn dialogues
# - Fine-tune model on specific domain
# - Add response quality filtering
