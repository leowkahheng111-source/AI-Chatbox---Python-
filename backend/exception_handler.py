"""
============================================================================
EXCEPTION HANDLER
============================================================================
Purpose: Global exception handling and error formatting
Usage: from backend.exception_handler import handle_exception
Interactions: Used by all modules to handle and log errors consistently
Expansion: Add specific exception types for different error scenarios
============================================================================
"""

# Standard Library Imports
import logging
import traceback
from typing import Dict, Optional, Any
from datetime import datetime

# Internal Project Imports
from config.constants import ResponseType, ERROR_MESSAGES


# Configure logger
logger = logging.getLogger(__name__)


class ChatbotException(Exception):
    """
    Base exception class for all chatbot-specific errors.
    
    Why: Allows catching all chatbot errors with one except block
    Design Pattern: Custom exception hierarchy
    
    Attributes:
        message: Error description
        error_code: Unique error identifier
        details: Additional error context
    """
    
    def __init__(
        self, 
        message: str, 
        error_code: str = "GENERAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize chatbot exception.
        
        Args:
            message: Human-readable error message
            error_code: Unique identifier for this error type
            details: Additional context (dict)
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary format.
        
        Returns:
            Dictionary with error details
            
        Why: Makes it easy to serialize errors for logging/API responses
        """
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }


# =============================================================================
# SPECIFIC EXCEPTION CLASSES
# =============================================================================

class ModuleException(ChatbotException):
    """
    Exception raised when a module fails to process a request.
    
    Usage:
        raise ModuleException("Calculator failed", error_code="CALC_001")
    """
    
    def __init__(self, message: str, module_name: str, **kwargs):
        self.module_name = module_name
        super().__init__(
            message=message,
            error_code=kwargs.get("error_code", "MODULE_ERROR"),
            details={"module_name": module_name, **kwargs.get("details", {})}
        )


class DatabaseException(ChatbotException):
    """Exception raised for database-related errors."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=kwargs.get("error_code", "DATABASE_ERROR"),
            details=kwargs.get("details", {})
        )


class ValidationException(ChatbotException):
    """Exception raised for input validation errors."""
    
    def __init__(self, message: str, field: str = None, **kwargs):
        details = kwargs.get("details", {})
        if field:
            details["field"] = field
        
        super().__init__(
            message=message,
            error_code=kwargs.get("error_code", "VALIDATION_ERROR"),
            details=details
        )


class SessionException(ChatbotException):
    """Exception raised for session-related errors."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=kwargs.get("error_code", "SESSION_ERROR"),
            details=kwargs.get("details", {})
        )


class FileProcessingException(ChatbotException):
    """Exception raised for file upload/processing errors."""
    
    def __init__(self, message: str, filename: str = None, **kwargs):
        details = kwargs.get("details", {})
        if filename:
            details["filename"] = filename
        
        super().__init__(
            message=message,
            error_code=kwargs.get("error_code", "FILE_ERROR"),
            details=details
        )


# =============================================================================
# EXCEPTION HANDLER
# =============================================================================

class ExceptionHandler:
    """
    Central exception handling system.
    
    Why: Provides consistent error handling across all modules
    Benefits:
        - Standardized error logging
        - User-friendly error messages
        - Detailed error tracking for debugging
    
    Usage:
        handler = ExceptionHandler()
        response = handler.handle(exception)
    """
    
    def __init__(self, debug_mode: bool = False):
        """
        Initialize exception handler.
        
        Args:
            debug_mode: If True, includes stack traces in responses
        """
        self.debug_mode = debug_mode
        self.logger = logging.getLogger(__name__)
    
    def handle(self, exception: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle an exception and return formatted error response.
        
        Args:
            exception: The exception to handle
            context: Additional context about where error occurred
            
        Returns:
            Dictionary with error information for user display
            
        Process:
            1. Log the error with full details
            2. Determine error type
            3. Format user-friendly message
            4. Return standardized error response
        """
        # Log the exception
        self._log_exception(exception, context)
        
        # Handle custom chatbot exceptions
        if isinstance(exception, ChatbotException):
            return self._handle_chatbot_exception(exception)
        
        # Handle standard Python exceptions
        return self._handle_standard_exception(exception)
    
    def _log_exception(self, exception: Exception, context: str) -> None:
        """
        Log exception with full details.
        
        Args:
            exception: The exception to log
            context: Where the error occurred
        """
        log_message = f"Exception in {context}: {str(exception)}"
        
        if isinstance(exception, ChatbotException):
            self.logger.error(
                f"{log_message}\nError Code: {exception.error_code}\n"
                f"Details: {exception.details}"
            )
        else:
            self.logger.error(log_message, exc_info=True)
    
    def _handle_chatbot_exception(
        self, 
        exception: ChatbotException
    ) -> Dict[str, Any]:
        """
        Handle custom chatbot exception.
        
        Args:
            exception: ChatbotException instance
            
        Returns:
            Formatted error response
        """
        response = {
            "type": ResponseType.ERROR.value,
            "message": exception.message,
            "error_code": exception.error_code,
            "timestamp": exception.timestamp.isoformat(),
        }
        
        # Include details only in debug mode
        if self.debug_mode:
            response["details"] = exception.details
        
        return response
    
    def _handle_standard_exception(
        self, 
        exception: Exception
    ) -> Dict[str, Any]:
        """
        Handle standard Python exception.
        
        Args:
            exception: Standard exception instance
            
        Returns:
            Formatted error response
        """
        # Map common exceptions to user-friendly messages
        error_mapping = {
            ValueError: "Invalid value provided",
            TypeError: "Invalid data type",
            KeyError: "Required data not found",
            FileNotFoundError: "File not found",
            PermissionError: "Permission denied",
            ConnectionError: "Connection failed",
        }
        
        user_message = error_mapping.get(
            type(exception),
            "An unexpected error occurred"
        )
        
        response = {
            "type": ResponseType.ERROR.value,
            "message": user_message,
            "error_code": "SYSTEM_ERROR",
            "timestamp": datetime.now().isoformat(),
        }
        
        # Include exception details in debug mode
        if self.debug_mode:
            response["details"] = {
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "traceback": traceback.format_exc(),
            }
        
        return response


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

# Global handler instance
_global_handler: Optional[ExceptionHandler] = None


def initialize_handler(debug_mode: bool = False) -> ExceptionHandler:
    """
    Initialize global exception handler.
    
    Args:
        debug_mode: Enable debug mode
        
    Returns:
        ExceptionHandler instance
        
    Usage:
        handler = initialize_handler(debug_mode=True)
    """
    global _global_handler
    _global_handler = ExceptionHandler(debug_mode=debug_mode)
    return _global_handler


def handle_exception(
    exception: Exception, 
    context: str = ""
) -> Dict[str, Any]:
    """
    Handle exception using global handler.
    
    Args:
        exception: Exception to handle
        context: Context information
        
    Returns:
        Formatted error response
        
    Usage:
        try:
            result = some_function()
        except Exception as e:
            error_response = handle_exception(e, "some_function")
    """
    global _global_handler
    
    if _global_handler is None:
        _global_handler = ExceptionHandler()
    
    return _global_handler.handle(exception, context)


def safe_execute(func, *args, **kwargs) -> tuple[bool, Any]:
    """
    Safely execute a function and handle any exceptions.
    
    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Tuple of (success: bool, result_or_error: Any)
        
    Usage:
        success, result = safe_execute(risky_function, arg1, arg2)
        if success:
            print(f"Result: {result}")
        else:
            print(f"Error: {result}")
    
    Why: Simplifies error handling in module code
    """
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        error_response = handle_exception(e, func.__name__)
        return False, error_response


# =============================================================================
# DECORATORS
# =============================================================================

def handle_errors(context: str = ""):
    """
    Decorator to automatically handle exceptions in functions.
    
    Args:
        context: Context description for logging
        
    Usage:
        @handle_errors("calculator_process")
        def calculate(expression):
            return eval(expression)
    
    Why: Reduces boilerplate try-except blocks
    Future: Add retry logic for transient errors
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ctx = context or func.__name__
                return handle_exception(e, ctx)
        return wrapper
    return decorator


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_not_empty(value: str, field_name: str) -> None:
    """
    Validate that a string value is not empty.
    
    Args:
        value: Value to validate
        field_name: Name of the field (for error message)
        
    Raises:
        ValidationException: If value is empty
        
    Usage:
        validate_not_empty(user_input, "message")
    """
    if not value or not value.strip():
        raise ValidationException(
            f"{field_name} cannot be empty",
            field=field_name
        )


def validate_max_length(value: str, max_length: int, field_name: str) -> None:
    """
    Validate that a string doesn't exceed maximum length.
    
    Args:
        value: Value to validate
        max_length: Maximum allowed length
        field_name: Name of the field
        
    Raises:
        ValidationException: If value exceeds max_length
    """
    if len(value) > max_length:
        raise ValidationException(
            f"{field_name} exceeds maximum length of {max_length}",
            field=field_name,
            details={"max_length": max_length, "actual_length": len(value)}
        )


# TODO: Add more validation helpers as needed
# - validate_file_size()
# - validate_file_type()
# - validate_email()
# - validate_api_key()
