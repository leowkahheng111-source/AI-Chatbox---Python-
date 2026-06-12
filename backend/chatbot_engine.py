"""
============================================================================
CHATBOT ENGINE
============================================================================
Purpose: Main controller and entry point for the chatbot system
Usage: from backend.chatbot_engine import ChatbotEngine
Interactions: Orchestrates all components (router, memory, database)
Expansion: Add conversation context, multi-turn dialogues, session management
============================================================================
"""

# Standard Library Imports
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Internal Project Imports
from backend.router import Router
from backend.intent_detector import IntentDetector
from backend.response_manager import ResponseManager
from backend.exception_handler import handle_errors, ChatbotException
from config.settings import Settings
from config.constants import RESPONSE_TEMPLATES


# Configure logger
logger = logging.getLogger(__name__)


class ChatbotEngine:
    """
    Main orchestrator for the chatbot system.
    
    Design Pattern: Facade Pattern (provides simple interface to complex system)
    
    Why this exists:
        - Single entry point for all chatbot operations
        - Coordinates all subsystems (router, memory, database)
        - Manages session lifecycle
        - Provides high-level API for frontend
    
    Architecture:
        Frontend (Streamlit) → ChatbotEngine → Router → Modules
                                    ↓
                            Memory + Database
    
    Responsibilities:
        1. Initialize all subsystems
        2. Handle session management
        3. Process user messages
        4. Coordinate responses
        5. Manage conversation state
        6. Log interactions
    
    Attributes:
        router: Routes requests to appropriate modules
        response_manager: Formats responses
        settings: Application configuration
        is_initialized: Whether engine is ready
    """
    
    def __init__(self):
        """
        Initialize chatbot engine.
        
        Process:
            1. Load configuration
            2. Initialize subsystems
            3. Set up logging
            4. Prepare for first request
        """
        self.logger = logging.getLogger(__name__)
        self.settings = Settings
        
        # Core components
        self.router: Optional[Router] = None
        self.response_manager: Optional[ResponseManager] = None
        
        # State management
        self.is_initialized = False
        self.start_time = datetime.now()
        
        # Initialize
        self._initialize()
    
    def _initialize(self) -> None:
        """
        Initialize all chatbot subsystems.
        
        Why separate method: Allows re-initialization if needed
        
        Steps:
            1. Initialize router
            2. Register modules
            3. Initialize response manager
            4. Initialize memory system (future)
            5. Connect to database (future)
        """
        try:
            self.logger.info("Initializing Chatbot Engine...")
            
            # Step 1: Initialize router
            self.router = Router()
            
            # Step 2: Register all available modules
            self._register_modules()
            
            # Step 3: Initialize response manager
            self.response_manager = ResponseManager()
            
            # Step 4: Set initialized flag
            self.is_initialized = True
            
            self.logger.info("Chatbot Engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Chatbot Engine: {e}", exc_info=True)
            raise ChatbotException(
                "Failed to initialize chatbot",
                error_code="INIT_ERROR",
                details={"error": str(e)}
            )
    
    def _register_modules(self) -> None:
        """
        Register all available skill modules with the router.
        
        Why: Keeps module registration centralized and organized
        
        Process:
            1. Import module classes
            2. Create module instances
            3. Register with router
        
        Future: Load modules dynamically from config or plugins folder
        """
        from modules.chat.chat_service import ChatService
        from modules.calculator.calculator_service import CalculatorService
        from modules.sql_helper.sql_service import SQLService
        from modules.powerbi_helper.dax_service import DAXService
        from modules.spss_helper.spss_service import SPSSService
        
        from config.constants import ModuleType
        
        # Register Chat module
        self.router.register_module(
            ModuleType.CHAT,
            ChatService()
        )
        
        # Register Calculator module
        self.router.register_module(
            ModuleType.CALCULATOR,
            CalculatorService()
        )
        
        # Register SQL Helper module
        self.router.register_module(
            ModuleType.SQL_HELPER,
            SQLService()
        )
        
        # Register Power BI DAX Helper module
        self.router.register_module(
            ModuleType.POWERBI_HELPER,
            DAXService()
        )
        
        # Register SPSS Helper module
        self.router.register_module(
            ModuleType.SPSS_HELPER,
            SPSSService()
        )
        
        self.logger.info(f"Registered {len(self.router.modules)} modules")
    
    @handle_errors("chatbot_engine_process")
    def process_message(
        self,
        user_message: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return response.
        
        Args:
            user_message: User's input message
            session_id: Optional session identifier
            user_id: Optional user identifier
            
        Returns:
            Response dictionary with chatbot's reply
            
        Process:
            1. Validate engine is initialized
            2. Validate input
            3. Route to appropriate module via router
            4. Store conversation in memory (future)
            5. Return formatted response
        
        Usage:
            engine = ChatbotEngine()
            response = engine.process_message("Calculate 2 + 2")
            print(response["content"])  # "4"
        """
        # Validation
        if not self.is_initialized:
            raise ChatbotException(
                "Chatbot engine not initialized",
                error_code="NOT_INITIALIZED"
            )
        
        if not user_message or not user_message.strip():
            return self.response_manager.create_error_response(
                "Please provide a message",
                error_code="EMPTY_MESSAGE"
            )
        
        self.logger.info(f"Processing message: {user_message[:50]}...")
        
        # Route message to appropriate module
        response = self.router.route(user_message, session_id=session_id)
        
        # TODO: Store conversation in memory/database
        # self._store_conversation(user_message, response, session_id, user_id)
        
        return response
    
    def get_welcome_message(self) -> Dict[str, Any]:
        """
        Get welcome message for new users/sessions.
        
        Returns:
            Welcome response dictionary
            
        Usage:
            welcome = engine.get_welcome_message()
            display(welcome["content"])
        
        Why: Provides consistent onboarding experience
        """
        return self.response_manager.apply_template("welcome")
    
    def get_available_skills(self) -> Dict[str, Any]:
        """
        Get list of available chatbot skills/modules.
        
        Returns:
            Response with skill information
            
        Usage:
            skills = engine.get_available_skills()
            # Shows what the chatbot can do
        
        Why: Helps users discover capabilities
        """
        available_modules = self.router.get_available_modules()
        
        skill_descriptions = {
            "chat": "💬 General conversation and questions",
            "calculator": "🧮 Mathematical calculations",
            "sql_helper": "🗃️ SQL query help and examples",
            "powerbi_helper": "📊 Power BI DAX formula assistance",
            "spss_helper": "📈 SPSS statistical analysis guidance",
        }
        
        skills_list = []
        for module in available_modules:
            module_value = module.value
            description = skill_descriptions.get(
                module_value,
                f"{module_value.replace('_', ' ').title()}"
            )
            skills_list.append(f"• {description}")
        
        content = "I can help you with:\n\n" + "\n".join(skills_list)
        
        return self.response_manager.create_info_response(content)
    
    def get_module_info(self) -> Dict[str, Any]:
        """
        Get detailed information about all modules.
        
        Returns:
            Dictionary with module status and details
            
        Usage:
            info = engine.get_module_info()
            # Shows which modules are active, planned, etc.
        
        Why: Useful for admin/debug views
        """
        module_info = self.router.get_module_info()
        
        return {
            "total_modules": len(module_info),
            "modules": module_info,
            "timestamp": datetime.now().isoformat(),
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get health status of the chatbot system.
        
        Returns:
            Health status dictionary
            
        Usage:
            health = engine.get_health_status()
            if health["status"] == "healthy":
                print("System OK")
        
        Why: Useful for monitoring, health checks, debugging
        """
        try:
            available_modules = self.router.get_available_modules()
            
            status = {
                "status": "healthy" if self.is_initialized else "unhealthy",
                "initialized": self.is_initialized,
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "available_modules": len(available_modules),
                "total_modules": len(self.router.modules),
                "timestamp": datetime.now().isoformat(),
            }
            
            return status
        
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
    
    def reset(self) -> None:
        """
        Reset the chatbot engine.
        
        Why: Useful for development, testing, or error recovery
        
        Warning: This clears all runtime state
        """
        self.logger.warning("Resetting chatbot engine...")
        self.is_initialized = False
        self._initialize()
        self.logger.info("Chatbot engine reset complete")
    
    def shutdown(self) -> None:
        """
        Gracefully shutdown the chatbot engine.
        
        Process:
            1. Close database connections (future)
            2. Save pending data (future)
            3. Clean up resources
        
        Usage:
            engine.shutdown()
        
        Why: Ensures clean shutdown and data persistence
        """
        self.logger.info("Shutting down chatbot engine...")
        
        # TODO: Close database connections
        # TODO: Save pending conversations
        # TODO: Clean up temporary files
        
        self.is_initialized = False
        self.logger.info("Chatbot engine shutdown complete")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

# Global engine instance (singleton pattern)
_global_engine: Optional[ChatbotEngine] = None


def get_engine() -> ChatbotEngine:
    """
    Get or create global chatbot engine instance.
    
    Returns:
        ChatbotEngine instance
        
    Why singleton: One engine instance per application
    
    Usage:
        from backend.chatbot_engine import get_engine
        engine = get_engine()
        response = engine.process_message("Hello!")
    """
    global _global_engine
    
    if _global_engine is None:
        _global_engine = ChatbotEngine()
    
    return _global_engine


def quick_chat(message: str) -> str:
    """
    Quick chat function for simple interactions.
    
    Args:
        message: User message
        
    Returns:
        Response content as string
        
    Usage:
        reply = quick_chat("Calculate 2 + 2")
        print(reply)  # "4"
    
    Why: Simplifies basic interactions, useful for testing
    """
    engine = get_engine()
    response = engine.process_message(message)
    return response.get("content", "No response")


# TODO: Future enhancements
# - Add conversation context (remember previous messages)
# - Implement session persistence
# - Add user preference management
# - Support for conversation branching
# - Implement rate limiting
# - Add analytics and usage tracking
# - Support for scheduled tasks/reminders
# - Multi-user conversation support
# - Voice input/output integration
# - Real-time streaming responses
