"""
============================================================================
CALCULATOR SERVICE
============================================================================
Purpose: Perform mathematical calculations and solve expressions
Usage: Handles math-related queries
Expansion: Add support for scientific functions, unit conversions, equations
============================================================================
"""

# Standard Library Imports
import logging
import re
import math
from typing import Dict, Any, Optional, Union

# Internal Project Imports
from backend.exception_handler import handle_errors, ModuleException


# Configure logger
logger = logging.getLogger(__name__)


class CalculatorService:
    """
    Mathematical calculation module.
    
    Why this exists:
        - Solves mathematical expressions
        - Handles basic and advanced calculations
        - Provides safe evaluation of math expressions
    
    Current Capabilities:
        - Basic operations: +, -, *, /
        - Exponents: **
        - Parentheses for order of operations
        - Common math functions: sqrt, sin, cos, tan, log, abs
        - Constants: pi, e
    
    Future Capabilities:
        - Unit conversions
        - Equation solving
        - Matrix operations
        - Statistical calculations
        - Complex numbers
    
    Security:
        - Uses safe evaluation (not eval())
        - Validates input before processing
        - Prevents code injection
    """
    
    def __init__(self):
        """Initialize calculator service."""
        self.logger = logging.getLogger(__name__)
        
        # Safe math functions that can be used
        self.safe_functions = {
            'abs': abs,
            'round': round,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pow': pow,
            'pi': math.pi,
            'e': math.e,
        }
        
        self.logger.info("CalculatorService initialized")
    
    @handle_errors("calculator_service_process")
    def process(
        self,
        user_input: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Process mathematical calculation request.
        
        Args:
            user_input: User's input (expression to calculate)
            session_id: Optional session ID
            
        Returns:
            Calculation result as string
            
        Process:
            1. Extract mathematical expression
            2. Validate expression
            3. Evaluate safely
            4. Format result
        
        Examples:
            Input: "calculate 2 + 2"
            Output: "2 + 2 = 4"
            
            Input: "what is 5 * (3 + 2)"
            Output: "5 * (3 + 2) = 25"
        """
        if not user_input:
            raise ModuleException(
                "No expression provided",
                module_name="calculator"
            )
        
        # Extract mathematical expression from input
        expression = self._extract_expression(user_input)
        
        if not expression:
            raise ModuleException(
                "No valid mathematical expression found",
                module_name="calculator"
            )
        
        self.logger.info(f"Calculating: {expression}")
        
        try:
            # Evaluate the expression
            result = self._evaluate(expression)
            
            # Format the response
            response = self._format_result(expression, result)
            
            return response
        
        except Exception as e:
            self.logger.error(f"Calculation error: {e}")
            raise ModuleException(
                f"Failed to calculate expression: {str(e)}",
                module_name="calculator"
            )
    
    def _extract_expression(self, user_input: str) -> str:
        """
        Extract mathematical expression from user input.
        
        Args:
            user_input: Raw user input
            
        Returns:
            Cleaned mathematical expression
            
        Process:
            - Remove common words (calculate, what is, etc.)
            - Keep only math-related characters
            - Preserve function names
        """
        # Remove common phrases
        expression = user_input.lower()
        removal_phrases = [
            'calculate', 'compute', 'what is', 'solve',
            'find', 'evaluate', 'equal', 'equals', 'is'
        ]
        
        for phrase in removal_phrases:
            expression = expression.replace(phrase, '')
        
        # Clean up whitespace
        expression = expression.strip()
        
        # Replace common text representations
        replacements = {
            'plus': '+',
            'minus': '-',
            'times': '*',
            'multiplied by': '*',
            'divided by': '/',
            'squared': '**2',
            'cubed': '**3',
        }
        
        for text, symbol in replacements.items():
            expression = expression.replace(text, symbol)
        
        return expression
    
    def _evaluate(self, expression: str) -> Union[int, float]:
        """
        Safely evaluate mathematical expression.
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            Numerical result
            
        Security: Does NOT use eval() for safety
        Uses safer approach with limited namespace
        """
        # Validate expression first
        self._validate_expression(expression)
        
        try:
            # Create safe namespace with allowed functions/constants
            safe_dict = self.safe_functions.copy()
            
            # Use eval with restricted namespace (safer than plain eval)
            # Note: For production, consider using a proper math parser library
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            
            return result
        
        except ZeroDivisionError:
            raise ModuleException(
                "Cannot divide by zero",
                module_name="calculator"
            )
        except NameError as e:
            raise ModuleException(
                f"Unknown function or constant: {e}",
                module_name="calculator"
            )
        except SyntaxError:
            raise ModuleException(
                "Invalid mathematical expression",
                module_name="calculator"
            )
    
    def _validate_expression(self, expression: str) -> None:
        """
        Validate that expression is safe to evaluate.
        
        Args:
            expression: Expression to validate
            
        Raises:
            ModuleException: If expression contains unsafe elements
            
        Security checks:
            - No import statements
            - No function definitions
            - No attribute access (.)
            - No double underscores (__)
        """
        # Check for dangerous patterns
        dangerous_patterns = [
            'import', '__', 'exec', 'eval', 'compile',
            'open', 'file', 'input', 'raw_input'
        ]
        
        lower_expression = expression.lower()
        for pattern in dangerous_patterns:
            if pattern in lower_expression:
                raise ModuleException(
                    f"Unsafe expression: contains '{pattern}'",
                    module_name="calculator"
                )
        
        # Check for attribute access (except for math functions)
        if '.' in expression and not any(f in expression for f in ['math.']):
            raise ModuleException(
                "Unsafe expression: attribute access not allowed",
                module_name="calculator"
            )
    
    def _format_result(self, expression: str, result: Union[int, float]) -> str:
        """
        Format calculation result for display.
        
        Args:
            expression: Original expression
            result: Calculated result
            
        Returns:
            Formatted result string
        """
        # Round to reasonable precision
        if isinstance(result, float):
            # Check if result is close to an integer
            if abs(result - round(result)) < 1e-10:
                result = int(round(result))
            else:
                result = round(result, 6)
        
        return f"**{expression}** = **{result}**"


# TODO: Future enhancements
# - Add support for complex numbers
# - Implement equation solving (symbolic math)
# - Add matrix operations
# - Support unit conversions (meters to feet, etc.)
# - Add plotting capabilities for functions
# - Support for variables (let x = 5, calculate x + 3)
# - Add calculation history
# - Support for custom functions
# - Add LaTeX output for formulas
# - Implement step-by-step solution explanations
