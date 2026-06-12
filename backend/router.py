"""
============================================================================
ROUTER
============================================================================
Purpose: Route user requests to the appropriate skill module
Usage: from backend.router import Router
Interactions: Receives intent from intent_detector, calls appropriate module
Expansion: Add module priority, fallback chains, parallel module execution
============================================================================
"""

# Standard Library Imports
import logging
from typing import Dict, Any, Optional

# Internal Project Imports
from config.constants import ModuleType, MODULE_STATUS_MAP, ModuleStatus
from backend.intent_detector import IntentDetector
from backend.response_manager import ResponseManager
from backend.exception_handler import ChatbotException, ModuleException


# Configure logger
logger = logging.getLogger(__name__)


class Router:
    """
    Routes user requests to appropriate skill modules.
    
    Design Pattern: Router Pattern + Factory Pattern
    
    Why this exists:
        - Central routing logic for all requests
        - Decouples modules from each other
        - Makes adding new modules easy (just register them)
        - Provides fallback handling
    
    Responsibilities:
        1. Receive user input
        2. Detect intent (which module to use)
        3. Route to appropriate module
        4. Handle module unavailability
        5. Format and return response
    
    Architecture Flow:
        User Input → Intent Detection → Module Selection →
        Module Execution → Response Formatting → Return
    
    Attributes:
        modules: Dictionary mapping ModuleType to module instances
        intent_detector: Intent detection system
        response_manager: Response formatting system
        default_module: Fallback when intent unclear (CHAT)
    """
    
    def __init__(self):
        """Initialize router with empty module registry."""
        self.modules: Dict[ModuleType, Any] = {}
        self.intent_detector = IntentDetector()
        self.response_manager = ResponseManager()
        self.default_module = ModuleType.CHAT
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Router initialized")
    
    def register_module(self, module_type: ModuleType, module_instance: Any) -> None:
        """
        Register a skill module with the router.
        
        Args:
            module_type: Type of module (from ModuleType enum)
            module_instance: Instance of the module class
            
        Why: Allows dynamic module registration without hardcoding
        
        Usage:
            router = Router()
            calculator = CalculatorService()
            router.register_module(ModuleType.CALCULATOR, calculator)
        
        Future: Load modules from config file or database
        """
        # Validate module has required interface
        if not hasattr(module_instance, 'process'):
            raise ValueError(
                f"Module {module_type.value} must have a 'process' method"
            )
        
        self.modules[module_type] = module_instance
        self.logger.info(f"Registered module: {module_type.value}")
    
    def route(self, user_input: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Route user input to appropriate module and return response.
        
        Args:
            user_input: User's message/query
            session_id: Optional session identifier for context
            
        Returns:
            Standardized response dictionary
            
        Process:
            1. Validate input
            2. Detect intent
            3. Check module availability
            4. Execute module
            5. Format response
            6. Handle errors
        
        Usage:
            router = Router()
            response = router.route("Calculate 2 + 2")
            print(response["content"])  # "4"
        """
        self.logger.info(f"Routing request: {user_input[:50]}...")
        
        try:
            # Step 1: Validate input
            if not user_input or not user_input.strip():
                return self.response_manager.create_error_response(
                    "Empty input received",
                    error_code="EMPTY_INPUT"
                )
            
            # Step 2: Detect intent
            intent, confidence = self.intent_detector.detect_with_confidence(user_input)
            
            self.logger.info(
                f"Intent detected: {intent.value} (confidence: {confidence:.2f})"
            )
            
            # Step 3: Get appropriate module
            module = self._get_module(intent)
            
            if module is None:
                return self._handle_unavailable_module(intent)
            
            # Step 4: Execute module
            try:
                module_output = module.process(user_input, session_id=session_id)
            except Exception as e:
                raise ModuleException(
                    message=f"Module processing failed: {str(e)}",
                    module_name=intent.value
                )
            
            # Step 5: Format response
            response = self.response_manager.format_module_response(
                module_output,
                module_name=intent.value
            )
            
            # Add routing metadata
            response["routing_info"] = {
                "detected_intent": intent.value,
                "confidence": confidence,
                "module_used": intent.value,
            }
            
            return response
        
        except ChatbotException as e:
            self.logger.error(f"Chatbot exception: {e.message}")
            return self.response_manager.create_error_response(
                e.message,
                error_code=e.error_code,
                details=e.details
            )
        
        except Exception as e:
            self.logger.error(f"Unexpected error in routing: {str(e)}", exc_info=True)
            return self.response_manager.create_error_response(
                "An unexpected error occurred. Please try again.",
                error_code="ROUTING_ERROR"
            )
    
    def _get_module(self, module_type: ModuleType) -> Optional[Any]:
        """
        Get module instance for given type.
        
        Args:
            module_type: Type of module needed
            
        Returns:
            Module instance or None if not available
            
        Why: Centralizes module retrieval and validation
        """
        # Check if module is registered
        if module_type not in self.modules:
            self.logger.warning(f"Module not registered: {module_type.value}")
            
            # Try default module as fallback
            if self.default_module in self.modules:
                self.logger.info(f"Falling back to default module: {self.default_module.value}")
                return self.modules[self.default_module]
            
            return None
        
        # Check if module is active
        status = MODULE_STATUS_MAP.get(module_type, ModuleStatus.PLANNED)
        if status != ModuleStatus.ACTIVE:
            self.logger.warning(
                f"Module {module_type.value} is {status.value}, not active"
            )
            return None
        
        return self.modules[module_type]
    
    def _handle_unavailable_module(self, module_type: ModuleType) -> Dict[str, Any]:
        """
        Handle requests for unavailable modules.
        
        Args:
            module_type: The unavailable module type
            
        Returns:
            Error response explaining unavailability
            
        Why: Provides helpful feedback instead of generic errors
        """
        status = MODULE_STATUS_MAP.get(module_type, ModuleStatus.PLANNED)
        
        messages = {
            ModuleStatus.DEVELOPMENT: (
                f"The {module_type.value} module is currently under development. "
                "It will be available soon!"
            ),
            ModuleStatus.PLANNED: (
                f"The {module_type.value} module is planned for a future release. "
                "Stay tuned!"
            ),
            ModuleStatus.DEPRECATED: (
                f"The {module_type.value} module is no longer supported. "
                "Please use an alternative."
            ),
        }
        
        message = messages.get(
            status,
            f"The {module_type.value} module is currently unavailable."
        )
        
        return self.response_manager.create_warning_response(
            message,
            module_name=module_type.value
        )
    
    def get_available_modules(self) -> list[ModuleType]:
        """
        Get list of all available (registered and active) modules.
        
        Returns:
            List of available module types
            
        Usage:
            available = router.get_available_modules()
            print("Available modules:", [m.value for m in available])
        
        Why: Useful for displaying capabilities to users
        """
        return [
            module_type
            for module_type in self.modules.keys()
            if MODULE_STATUS_MAP.get(module_type) == ModuleStatus.ACTIVE
        ]
    
    def is_module_available(self, module_type: ModuleType) -> bool:
        """
        Check if a specific module is available.
        
        Args:
            module_type: Module to check
            
        Returns:
            True if available, False otherwise
        """
        return (
            module_type in self.modules and
            MODULE_STATUS_MAP.get(module_type) == ModuleStatus.ACTIVE
        )
    
    def set_default_module(self, module_type: ModuleType) -> None:
        """
        Set the default fallback module.
        
        Args:
            module_type: Module to use as default
            
        Why: Allows customization of fallback behavior
        
        Usage:
            router.set_default_module(ModuleType.CHAT)
        """
        if module_type in self.modules:
            self.default_module = module_type
            self.logger.info(f"Default module set to: {module_type.value}")
        else:
            raise ValueError(f"Module {module_type.value} not registered")
    
    def get_module_info(self) -> Dict[str, Any]:
        """
        Get information about all registered modules.
        
        Returns:
            Dictionary with module status information
            
        Usage:
            info = router.get_module_info()
            for module, data in info.items():
                print(f"{module}: {data['status']}")
        
        Why: Useful for admin panels, debugging, health checks
        """
        info = {}
        
        for module_type in ModuleType:
            if module_type == ModuleType.UNKNOWN:
                continue
            
            info[module_type.value] = {
                "registered": module_type in self.modules,
                "status": MODULE_STATUS_MAP.get(module_type, ModuleStatus.PLANNED).value,
                "available": self.is_module_available(module_type),
            }
        
        return info
    
    def unregister_module(self, module_type: ModuleType) -> None:
        """
        Unregister a module from the router.
        
        Args:
            module_type: Module to unregister
            
        Why: Allows dynamic module management, useful for updates/maintenance
        
        Usage:
            router.unregister_module(ModuleType.CALCULATOR)
        """
        if module_type in self.modules:
            del self.modules[module_type]
            self.logger.info(f"Unregistered module: {module_type.value}")
        else:
            self.logger.warning(f"Module not registered: {module_type.value}")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

# Global router instance (singleton pattern)
_global_router: Optional[Router] = None


def get_router() -> Router:
    """
    Get or create global router instance.
    
    Returns:
        Router instance
        
    Usage:
        from backend.router import get_router
        router = get_router()
        response = router.route("Calculate 2 + 2")
    """
    global _global_router
    
    if _global_router is None:
        _global_router = Router()
    
    return _global_router


def quick_route(user_input: str) -> Dict[str, Any]:
    """
    Quick routing using global router.
    
    Args:
        user_input: User's message
        
    Returns:
        Response dictionary
        
    Usage:
        response = quick_route("What is SQL JOIN?")
        print(response["content"])
    """
    router = get_router()
    return router.route(user_input)


# TODO: Future enhancements
# - Module priority/preference system
# - Parallel module execution for multi-intent
# - Module health checking and circuit breakers
# - Request rate limiting per module
# - Module load balancing
# - Conditional routing based on user preferences
# - A/B testing for routing strategies
# - Module caching for frequently used modules
