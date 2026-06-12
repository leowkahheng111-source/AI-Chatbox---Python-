"""
============================================================================
RESPONSE MANAGER
============================================================================
Purpose: Format and standardize all chatbot responses
Usage: from backend.response_manager import ResponseManager
Interactions: Receives module output, formats for UI display
Expansion: Add response templates, multi-language support, rich formatting
============================================================================
"""

# Standard Library Imports
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Internal Project Imports
from config.constants import ResponseType, RESPONSE_TEMPLATES


# Configure logger
logger = logging.getLogger(__name__)


class ResponseManager:
    """
    Manages formatting and delivery of chatbot responses.
    
    Why this exists:
        - Ensures consistent response format across all modules
        - Separates presentation logic from business logic
        - Makes it easy to change response format globally
        - Adds metadata (timestamps, response IDs) automatically
    
    Design Pattern: Facade Pattern (simplifies response creation)
    
    Responsibilities:
        1. Format module output into standard response structure
        2. Add metadata (timestamps, IDs, type)
        3. Apply response templates
        4. Handle error responses
        5. Sanitize output for safe display
    
    Future enhancements:
        - Response caching
        - Multi-language support
        - Rich formatting (markdown, HTML)
        - Response personalization
        - A/B testing for response formats
    """
    
    def __init__(self):
        """Initialize response manager."""
        self.logger = logging.getLogger(__name__)
        self._response_counter = 0  # Track response count for IDs
    
    def create_response(
        self,
        content: str,
        response_type: ResponseType = ResponseType.SUCCESS,
        metadata: Optional[Dict[str, Any]] = None,
        module_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized response structure.
        
        Args:
            content: The main response content
            response_type: Type of response (success/error/info/warning)
            metadata: Additional metadata to include
            module_name: Name of module that generated this response
            
        Returns:
            Standardized response dictionary
            
        Response Structure:
            {
                "response_id": "unique_id",
                "type": "success",
                "content": "response text",
                "timestamp": "ISO timestamp",
                "module": "calculator",
                "metadata": {...}
            }
        
        Usage:
            response = manager.create_response(
                content="The result is 42",
                response_type=ResponseType.SUCCESS,
                module_name="calculator"
            )
        """
        self._response_counter += 1
        
        response = {
            "response_id": self._generate_response_id(),
            "type": response_type.value,
            "content": self._sanitize_content(content),
            "timestamp": datetime.now().isoformat(),
        }
        
        # Add optional fields
        if module_name:
            response["module"] = module_name
        
        if metadata:
            response["metadata"] = metadata
        
        self.logger.debug(
            f"Created response #{self._response_counter} "
            f"[{response_type.value}] from {module_name or 'unknown'}"
        )
        
        return response
    
    def create_success_response(
        self,
        content: str,
        module_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a success response.
        
        Args:
            content: Response content
            module_name: Module that generated this
            **kwargs: Additional metadata
            
        Returns:
            Success response dictionary
            
        Usage:
            response = manager.create_success_response(
                "Calculation complete: 42",
                module_name="calculator"
            )
        """
        return self.create_response(
            content=content,
            response_type=ResponseType.SUCCESS,
            module_name=module_name,
            metadata=kwargs
        )
    
    def create_error_response(
        self,
        error_message: str,
        error_code: Optional[str] = None,
        module_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an error response.
        
        Args:
            error_message: User-friendly error message
            error_code: Error code for tracking
            module_name: Module where error occurred
            details: Additional error details
            
        Returns:
            Error response dictionary
            
        Usage:
            response = manager.create_error_response(
                error_message="Invalid expression",
                error_code="CALC_001",
                module_name="calculator"
            )
        """
        metadata = {}
        if error_code:
            metadata["error_code"] = error_code
        if details:
            metadata["details"] = details
        
        return self.create_response(
            content=error_message,
            response_type=ResponseType.ERROR,
            module_name=module_name,
            metadata=metadata
        )
    
    def create_info_response(
        self,
        content: str,
        module_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an informational response.
        
        Args:
            content: Information to display
            module_name: Source module
            
        Returns:
            Info response dictionary
            
        Usage: For non-critical information, tips, or guidance
        """
        return self.create_response(
            content=content,
            response_type=ResponseType.INFO,
            module_name=module_name
        )
    
    def create_warning_response(
        self,
        content: str,
        module_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a warning response.
        
        Args:
            content: Warning message
            module_name: Source module
            
        Returns:
            Warning response dictionary
            
        Usage: For situations that need user attention but aren't errors
        """
        return self.create_response(
            content=content,
            response_type=ResponseType.WARNING,
            module_name=module_name
        )
    
    def format_module_response(
        self,
        module_output: Any,
        module_name: str
    ) -> Dict[str, Any]:
        """
        Format output from a module into standard response.
        
        Args:
            module_output: Raw output from module
            module_name: Name of the module
            
        Returns:
            Formatted response dictionary
            
        Why: Modules can return different formats, this normalizes them
        
        Handles:
            - String output (simple text)
            - Dictionary output (structured data)
            - Error dictionaries
            - None/empty output
        """
        # Handle None or empty output
        if module_output is None:
            return self.create_error_response(
                "Module returned no output",
                module_name=module_name
            )
        
        # Handle dictionary output (already structured)
        if isinstance(module_output, dict):
            # Check if it's an error dictionary
            if module_output.get("type") == ResponseType.ERROR.value:
                return self.create_error_response(
                    module_output.get("message", "Unknown error"),
                    error_code=module_output.get("error_code"),
                    module_name=module_name,
                    details=module_output.get("details")
                )
            
            # Check if it has content field
            if "content" in module_output:
                return self.create_success_response(
                    module_output["content"],
                    module_name=module_name,
                    **module_output.get("metadata", {})
                )
            
            # Convert entire dict to string for display
            content = self._format_dict_as_text(module_output)
            return self.create_success_response(
                content,
                module_name=module_name
            )
        
        # Handle string output (most common)
        if isinstance(module_output, str):
            return self.create_success_response(
                module_output,
                module_name=module_name
            )
        
        # Handle other types (convert to string)
        return self.create_success_response(
            str(module_output),
            module_name=module_name
        )
    
    def apply_template(
        self,
        template_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Apply a predefined response template.
        
        Args:
            template_name: Name of template from constants
            **kwargs: Variables to inject into template
            
        Returns:
            Response using the template
            
        Usage:
            response = manager.apply_template(
                "welcome",
                user_name="John"
            )
        
        Why: Consistent messaging for common scenarios
        """
        template = RESPONSE_TEMPLATES.get(template_name)
        
        if not template:
            self.logger.warning(f"Template not found: {template_name}")
            return self.create_error_response(
                "Template not found",
                error_code="TEMPLATE_NOT_FOUND"
            )
        
        # Format template with provided variables
        try:
            content = template.format(**kwargs)
        except KeyError as e:
            self.logger.error(f"Missing template variable: {e}")
            content = template
        
        return self.create_info_response(content)
    
    def create_multi_part_response(
        self,
        parts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a response with multiple parts.
        
        Args:
            parts: List of response parts
            
        Returns:
            Multi-part response dictionary
            
        Usage:
            response = manager.create_multi_part_response([
                {"title": "Result", "content": "42"},
                {"title": "Explanation", "content": "The answer"}
            ])
        
        Why: For complex responses with multiple sections
        Future: Used for analytics, reports, visualizations
        """
        return {
            "response_id": self._generate_response_id(),
            "type": ResponseType.SUCCESS.value,
            "multipart": True,
            "parts": parts,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _generate_response_id(self) -> str:
        """
        Generate unique response ID.
        
        Returns:
            Unique response identifier
            
        Format: RESP_YYYYMMDD_HHMMSS_COUNT
        Example: RESP_20240101_143022_0001
        
        Why: Helps track responses in logs and database
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"RESP_{timestamp}_{self._response_counter:04d}"
    
    def _sanitize_content(self, content: str) -> str:
        """
        Sanitize response content for safe display.
        
        Args:
            content: Raw content
            
        Returns:
            Sanitized content
            
        Why: Prevents injection attacks, removes sensitive data
        
        Current: Basic sanitization
        Future: Add HTML escaping, markdown sanitization
        """
        if not isinstance(content, str):
            content = str(content)
        
        # Remove null bytes
        content = content.replace("\x00", "")
        
        # Limit length to prevent UI issues
        max_length = 10000
        if len(content) > max_length:
            content = content[:max_length] + "\n... (truncated)"
            self.logger.warning(f"Response content truncated (exceeded {max_length} chars)")
        
        return content
    
    def _format_dict_as_text(self, data: Dict[str, Any], indent: int = 0) -> str:
        """
        Format dictionary as readable text.
        
        Args:
            data: Dictionary to format
            indent: Indentation level
            
        Returns:
            Formatted string representation
            
        Why: Makes structured data readable in chat UI
        """
        lines = []
        indent_str = "  " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{key}:")
                lines.append(self._format_dict_as_text(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{indent_str}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(self._format_dict_as_text(item, indent + 1))
                    else:
                        lines.append(f"{indent_str}  - {item}")
            else:
                lines.append(f"{indent_str}{key}: {value}")
        
        return "\n".join(lines)
    
    def extract_content(self, response: Dict[str, Any]) -> str:
        """
        Extract displayable content from response.
        
        Args:
            response: Response dictionary
            
        Returns:
            Content string for display
            
        Why: UI layer can get clean content without parsing structure
        
        Usage:
            content = manager.extract_content(response)
            print(content)  # Just the message, no metadata
        """
        if "content" in response:
            return response["content"]
        
        if "parts" in response:
            # Multi-part response
            return "\n\n".join(
                part.get("content", "") for part in response["parts"]
            )
        
        return str(response)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

# Global response manager instance
_global_manager: Optional[ResponseManager] = None


def get_response_manager() -> ResponseManager:
    """
    Get or create global response manager instance.
    
    Returns:
        ResponseManager instance
        
    Usage:
        from backend.response_manager import get_response_manager
        manager = get_response_manager()
        response = manager.create_success_response("Done!")
    """
    global _global_manager
    
    if _global_manager is None:
        _global_manager = ResponseManager()
    
    return _global_manager


def quick_success(content: str, module: str = None) -> Dict[str, Any]:
    """Quick success response creation."""
    manager = get_response_manager()
    return manager.create_success_response(content, module_name=module)


def quick_error(message: str, module: str = None) -> Dict[str, Any]:
    """Quick error response creation."""
    manager = get_response_manager()
    return manager.create_error_response(message, module_name=module)


# TODO: Future enhancements
# - Add response caching for common queries
# - Implement multi-language support
# - Add rich formatting (markdown, HTML)
# - Support for embedded images/files
# - Response templates from database
# - User preference for response format
# - Response analytics and tracking
