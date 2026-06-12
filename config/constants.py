"""
============================================================================
APPLICATION CONSTANTS
============================================================================
Purpose: Define global constants used throughout the application
Usage: from config.constants import MODULE_TYPES
Interactions: Referenced by router, intent detector, and modules
Expansion: Add new module types and intents as features are added
============================================================================
"""

# Standard Library Imports
from enum import Enum
from typing import Dict, List


# =============================================================================
# MODULE TYPES
# =============================================================================
class ModuleType(Enum):
    """
    Enum for chatbot module types.
    
    Why Enum: Type-safe, prevents typos, auto-completion in IDEs
    
    Usage:
        from config.constants import ModuleType
        if intent == ModuleType.CALCULATOR:
            ...
    """
    CHAT = "chat"
    CALCULATOR = "calculator"
    SQL_HELPER = "sql_helper"
    POWERBI_HELPER = "powerbi_helper"
    SPSS_HELPER = "spss_helper"
    CSV_ANALYZER = "csv_analyzer"  # Future
    EXCEL_ANALYZER = "excel_analyzer"  # Future
    PDF_READER = "pdf_reader"  # Future
    UNKNOWN = "unknown"


# =============================================================================
# INTENT KEYWORDS
# =============================================================================
# Purpose: Keywords used by intent detector to route requests
# Structure: Dict[ModuleType, List[keywords]]

INTENT_KEYWORDS: Dict[ModuleType, List[str]] = {
    ModuleType.CALCULATOR: [
        "calculate", "compute", "math", "add", "subtract", "multiply",
        "divide", "sum", "total", "equation", "solve", "+", "-", "*", "/",
        "percentage", "average", "mean"
    ],
    
    ModuleType.SQL_HELPER: [
        "sql", "query", "database", "select", "insert", "update", "delete",
        "join", "where", "table", "mysql", "postgresql", "sqlite",
        "group by", "order by", "create table"
    ],
    
    ModuleType.POWERBI_HELPER: [
        "dax", "power bi", "powerbi", "measure", "calculate", "filter",
        "sumx", "related", "all", "allexcept", "row context", "filter context",
        "time intelligence", "earlier"
    ],
    
    ModuleType.SPSS_HELPER: [
        "spss", "statistics", "regression", "anova", "correlation",
        "chi-square", "t-test", "crosstab", "frequencies", "descriptives",
        "factor analysis", "reliability", "normality"
    ],
    
    # Future modules
    ModuleType.CSV_ANALYZER: [
        "csv", "analyze csv", "data analysis", "analyze data",
        "summarize data", "statistics csv"
    ],
    
    ModuleType.EXCEL_ANALYZER: [
        "excel", "xlsx", "spreadsheet", "analyze excel", "pivot table"
    ],
    
    ModuleType.PDF_READER: [
        "pdf", "read pdf", "extract pdf", "parse pdf"
    ],
}


# =============================================================================
# RESPONSE TEMPLATES
# =============================================================================
# Purpose: Standardized response formats for consistency

class ResponseType(Enum):
    """Types of responses the chatbot can generate."""
    SUCCESS = "success"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"


RESPONSE_TEMPLATES: Dict[str, str] = {
    "welcome": """
    👋 Welcome to Mini AI Chatbox!
    
    I can help you with:
    💬 General conversation
    🧮 Mathematical calculations
    🗃️ SQL queries and database help
    📊 Power BI DAX formulas
    📈 SPSS statistical analysis
    
    What would you like help with today?
    """,
    
    "unknown_intent": """
    I'm not sure what you're asking for. I can help with:
    - Calculator: "Calculate 25 * 4"
    - SQL: "How do I join two tables?"
    - DAX: "Explain CALCULATE function"
    - SPSS: "How to run t-test?"
    - General chat: Just chat with me!
    """,
    
    "error": "❌ An error occurred: {error_message}",
    
    "module_unavailable": """
    ⚠️ The {module_name} module is currently under development.
    It will be available in a future update!
    """,
}


# =============================================================================
# ERROR MESSAGES
# =============================================================================
ERROR_MESSAGES: Dict[str, str] = {
    "database_error": "Failed to access database. Please try again.",
    "module_error": "Module processing failed: {details}",
    "invalid_input": "Invalid input provided. Please check your request.",
    "session_expired": "Your session has expired. Please start a new conversation.",
    "file_upload_error": "Failed to upload file: {details}",
    "file_size_exceeded": "File size exceeds maximum limit of {max_size}MB.",
    "unsupported_file_type": "File type not supported. Allowed types: {allowed_types}",
}


# =============================================================================
# VALIDATION RULES
# =============================================================================
class ValidationRules:
    """
    Validation constants for user inputs.
    
    Why: Centralized validation prevents security issues and bugs
    """
    
    # Text input validation
    MIN_MESSAGE_LENGTH: int = 1
    MAX_MESSAGE_LENGTH: int = 5000
    
    # File upload validation
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
    
    # Session validation
    MAX_SESSIONS_PER_USER: int = 5
    SESSION_TIMEOUT_SECONDS: int = 3600  # 1 hour
    
    # History validation
    MAX_HISTORY_MESSAGES: int = 100


# =============================================================================
# MODULE STATUS
# =============================================================================
class ModuleStatus(Enum):
    """Status of each module in the system."""
    ACTIVE = "active"          # Fully functional
    DEVELOPMENT = "development"  # Under development
    PLANNED = "planned"        # Future implementation
    DEPRECATED = "deprecated"  # No longer supported


# Module implementation status tracking
MODULE_STATUS_MAP: Dict[ModuleType, ModuleStatus] = {
    ModuleType.CHAT: ModuleStatus.ACTIVE,
    ModuleType.CALCULATOR: ModuleStatus.ACTIVE,
    ModuleType.SQL_HELPER: ModuleStatus.ACTIVE,
    ModuleType.POWERBI_HELPER: ModuleStatus.ACTIVE,
    ModuleType.SPSS_HELPER: ModuleStatus.ACTIVE,
    ModuleType.CSV_ANALYZER: ModuleStatus.PLANNED,
    ModuleType.EXCEL_ANALYZER: ModuleStatus.PLANNED,
    ModuleType.PDF_READER: ModuleStatus.PLANNED,
}


# =============================================================================
# LOGGING CONSTANTS
# =============================================================================
class LogMessages:
    """Standard log messages for consistency."""
    
    # Startup
    APP_STARTED = "Application started successfully"
    APP_SHUTDOWN = "Application shutting down"
    
    # Module events
    MODULE_LOADED = "Module loaded: {module_name}"
    MODULE_PROCESSING = "Processing request with module: {module_name}"
    MODULE_ERROR = "Module error in {module_name}: {error}"
    
    # User events
    USER_MESSAGE_RECEIVED = "User message received: {message_preview}"
    RESPONSE_SENT = "Response sent to user"
    
    # Database events
    DB_CONNECTED = "Database connected successfully"
    DB_QUERY_EXECUTED = "Database query executed: {query}"
    DB_ERROR = "Database error: {error}"


# =============================================================================
# UI CONSTANTS
# =============================================================================
class UIConstants:
    """Constants for the user interface."""
    
    # Streamlit page configuration
    PAGE_TITLE = "Mini AI Chatbox"
    PAGE_ICON = "🤖"
    LAYOUT = "wide"
    
    # Theme colors (for custom styling)
    PRIMARY_COLOR = "#0066CC"
    SECONDARY_COLOR = "#FF6B6B"
    SUCCESS_COLOR = "#51CF66"
    WARNING_COLOR = "#FFA94D"
    ERROR_COLOR = "#FF6B6B"
    
    # Chat display
    MAX_DISPLAY_MESSAGES = 50
    MESSAGE_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_module_status(module_type: ModuleType) -> ModuleStatus:
    """
    Get the current status of a module.
    
    Args:
        module_type: The module to check
        
    Returns:
        Current status of the module
        
    Usage:
        status = get_module_status(ModuleType.CALCULATOR)
        if status == ModuleStatus.ACTIVE:
            ...
    """
    return MODULE_STATUS_MAP.get(module_type, ModuleStatus.PLANNED)


def is_module_active(module_type: ModuleType) -> bool:
    """
    Check if a module is active and ready to use.
    
    Args:
        module_type: The module to check
        
    Returns:
        True if module is active, False otherwise
    """
    return get_module_status(module_type) == ModuleStatus.ACTIVE


def get_active_modules() -> List[ModuleType]:
    """
    Get list of all active modules.
    
    Returns:
        List of active module types
        
    Usage:
        active_modules = get_active_modules()
        for module in active_modules:
            print(module.value)
    """
    return [
        module_type
        for module_type, status in MODULE_STATUS_MAP.items()
        if status == ModuleStatus.ACTIVE
    ]
