"""
============================================================================
INTENT DETECTOR
============================================================================
Purpose: Analyze user input and determine which module should handle it
Usage: from backend.intent_detector import IntentDetector
Interactions: Called by router to determine request routing
Expansion: Implement ML-based intent classification, support multi-intent
============================================================================
"""

# Standard Library Imports
import re
import logging
from typing import Optional, Dict, List, Tuple

# Internal Project Imports
from config.constants import ModuleType, INTENT_KEYWORDS
from backend.exception_handler import handle_errors


# Configure logger
logger = logging.getLogger(__name__)


class IntentDetector:
    """
    Detects user intent from input text to route to appropriate module.
    
    Design Pattern: Strategy Pattern (different detection strategies)
    
    Why this exists:
        - Centralizes routing logic
        - Makes it easy to improve detection algorithms
        - Separates intent detection from module execution
    
    Detection Strategy (Current):
        1. Keyword matching (simple but effective)
        2. Pattern matching (for math expressions)
        3. Confidence scoring
    
    Future Improvements:
        - Machine learning classification
        - Context-aware detection (remember previous intents)
        - Multi-intent support (one message, multiple modules)
        - Natural language understanding (NLU)
    
    Attributes:
        keywords: Mapping of module types to trigger keywords
        confidence_threshold: Minimum confidence to classify intent
    """
    
    def __init__(self, confidence_threshold: float = 0.3):
        """
        Initialize intent detector.
        
        Args:
            confidence_threshold: Minimum confidence (0-1) to classify
                                Higher = more strict, fewer false positives
                                Lower = more lenient, might misclassify
        
        Why 0.3: Balances accuracy and coverage for keyword matching
        """
        self.keywords = INTENT_KEYWORDS
        self.confidence_threshold = confidence_threshold
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"IntentDetector initialized with threshold: {confidence_threshold}")
    
    @handle_errors("detect_intent")
    def detect(self, user_input: str) -> ModuleType:
        """
        Detect the primary intent from user input.
        
        Args:
            user_input: The user's message/query
            
        Returns:
            ModuleType enum indicating which module should handle this
            
        Process:
            1. Normalize input (lowercase, clean)
            2. Check for special patterns (math expressions)
            3. Score each module based on keyword matches
            4. Return highest scoring module above threshold
            5. Default to CHAT if no clear match
        
        Usage:
            detector = IntentDetector()
            intent = detector.detect("Calculate 2 + 2")
            # Returns: ModuleType.CALCULATOR
        """
        # Input validation
        if not user_input or not user_input.strip():
            self.logger.warning("Empty input received")
            return ModuleType.CHAT
        
        # Normalize input
        normalized_input = self._normalize_input(user_input)
        
        self.logger.debug(f"Detecting intent for: {normalized_input[:50]}...")
        
        # Check for special patterns first (higher priority)
        special_intent = self._check_special_patterns(normalized_input)
        if special_intent:
            self.logger.info(f"Special pattern detected: {special_intent}")
            return special_intent
        
        # Score each module based on keyword matching
        scores = self._score_modules(normalized_input)
        
        # Find the best match
        best_intent, confidence = self._get_best_match(scores)
        
        self.logger.info(
            f"Intent detected: {best_intent.value} "
            f"(confidence: {confidence:.2f})"
        )
        
        return best_intent
    
    def detect_with_confidence(
        self, 
        user_input: str
    ) -> Tuple[ModuleType, float]:
        """
        Detect intent and return confidence score.
        
        Args:
            user_input: The user's message
            
        Returns:
            Tuple of (ModuleType, confidence_score)
            
        Why: Useful for showing certainty to users or logging
        
        Usage:
            intent, confidence = detector.detect_with_confidence("sql query")
            if confidence < 0.5:
                print("I'm not very confident about this...")
        """
        if not user_input or not user_input.strip():
            return ModuleType.CHAT, 1.0
        
        normalized_input = self._normalize_input(user_input)
        
        # Check special patterns
        special_intent = self._check_special_patterns(normalized_input)
        if special_intent:
            return special_intent, 1.0
        
        # Score modules
        scores = self._score_modules(normalized_input)
        best_intent, confidence = self._get_best_match(scores)
        
        return best_intent, confidence
    
    def _normalize_input(self, user_input: str) -> str:
        """
        Normalize user input for better matching.
        
        Args:
            user_input: Raw user input
            
        Returns:
            Normalized string (lowercase, trimmed)
            
        Why: Makes keyword matching case-insensitive and consistent
        """
        # Convert to lowercase
        normalized = user_input.lower().strip()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized
    
    def _check_special_patterns(self, text: str) -> Optional[ModuleType]:
        """
        Check for special patterns that indicate specific modules.
        
        Args:
            text: Normalized input text
            
        Returns:
            ModuleType if special pattern found, None otherwise
            
        Why: Some intents are better detected by pattern than keywords
        
        Patterns checked:
            - Math expressions: numbers and operators
            - SQL keywords: SELECT, INSERT, etc.
        """
        # Pattern 1: Math expression detection
        # Looks for: numbers, operators (+, -, *, /), parentheses
        math_pattern = r'[\d\+\-\*/\(\)\.\s]+'
        if re.search(r'\d+\s*[\+\-\*/]\s*\d+', text):
            # Contains at least "number operator number"
            return ModuleType.CALCULATOR
        
        # Pattern 2: SQL query detection
        # Starts with common SQL commands
        sql_keywords = ['select ', 'insert ', 'update ', 'delete ', 'create table']
        for keyword in sql_keywords:
            if text.startswith(keyword):
                return ModuleType.SQL_HELPER
        
        # Pattern 3: DAX function detection
        # Contains DAX function names in specific format
        if re.search(r'(calculate|sumx|filter|related|all)\s*\(', text):
            return ModuleType.POWERBI_HELPER
        
        return None
    
    def _score_modules(self, text: str) -> Dict[ModuleType, float]:
        """
        Score each module based on keyword matches.
        
        Args:
            text: Normalized input text
            
        Returns:
            Dictionary mapping ModuleType to confidence scores (0-1)
            
        Scoring algorithm:
            - Each keyword match adds to score
            - Score normalized by total words in input
            - Prevents long messages from having unfair advantage
        
        Example:
            Input: "help me with sql select query"
            Matches: sql=1, select=1, query=1
            Score: 3 matches / 6 words = 0.5
        """
        scores: Dict[ModuleType, float] = {}
        
        # Tokenize input (split into words)
        words = text.split()
        total_words = len(words)
        
        if total_words == 0:
            return scores
        
        # Score each module
        for module_type, keywords in self.keywords.items():
            matches = 0
            
            # Count keyword matches
            for keyword in keywords:
                # Check if keyword appears in text
                if keyword in text:
                    matches += 1
                    
                    # Bonus points if keyword is a whole word (not part of another word)
                    if f" {keyword} " in f" {text} ":
                        matches += 0.5
            
            # Normalize score by input length
            # Prevents bias toward modules with many keywords
            if matches > 0:
                score = min(matches / total_words, 1.0)
                scores[module_type] = score
        
        return scores
    
    def _get_best_match(
        self, 
        scores: Dict[ModuleType, float]
    ) -> Tuple[ModuleType, float]:
        """
        Find the module with highest confidence score.
        
        Args:
            scores: Dictionary of module scores
            
        Returns:
            Tuple of (best_module, confidence_score)
            
        Logic:
            - If no scores above threshold: return CHAT (default)
            - If one clear winner: return that module
            - If tie: return CHAT (safer to default)
        """
        if not scores:
            return ModuleType.CHAT, 1.0
        
        # Find highest scoring module
        best_module = max(scores, key=scores.get)
        confidence = scores[best_module]
        
        # Check if confidence meets threshold
        if confidence < self.confidence_threshold:
            self.logger.debug(
                f"Best match {best_module.value} below threshold "
                f"({confidence:.2f} < {self.confidence_threshold})"
            )
            return ModuleType.CHAT, confidence
        
        return best_module, confidence
    
    def get_all_scores(self, user_input: str) -> Dict[ModuleType, float]:
        """
        Get confidence scores for all modules.
        
        Args:
            user_input: User's message
            
        Returns:
            Dictionary of all module scores
            
        Why: Useful for debugging, analytics, or showing alternatives
        
        Usage:
            scores = detector.get_all_scores("calculate sum")
            for module, score in scores.items():
                print(f"{module.value}: {score:.2f}")
        """
        normalized_input = self._normalize_input(user_input)
        return self._score_modules(normalized_input)
    
    def add_custom_keywords(
        self, 
        module_type: ModuleType, 
        keywords: List[str]
    ) -> None:
        """
        Add custom keywords for a module.
        
        Args:
            module_type: Module to add keywords to
            keywords: List of new keywords
            
        Why: Allows runtime customization without changing constants
        
        Usage:
            detector.add_custom_keywords(
                ModuleType.CALCULATOR,
                ["compute", "arithmetic"]
            )
        
        Future: Load custom keywords from database or config file
        """
        if module_type in self.keywords:
            self.keywords[module_type].extend(keywords)
        else:
            self.keywords[module_type] = keywords
        
        self.logger.info(
            f"Added {len(keywords)} keywords to {module_type.value}"
        )


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

# Global detector instance (singleton pattern)
_global_detector: Optional[IntentDetector] = None


def get_detector() -> IntentDetector:
    """
    Get or create global intent detector instance.
    
    Returns:
        IntentDetector instance
        
    Why singleton: Avoid creating multiple detectors with same config
    
    Usage:
        from backend.intent_detector import get_detector
        detector = get_detector()
        intent = detector.detect("calculate 2+2")
    """
    global _global_detector
    
    if _global_detector is None:
        _global_detector = IntentDetector()
    
    return _global_detector


def quick_detect(user_input: str) -> ModuleType:
    """
    Quick intent detection using global detector.
    
    Args:
        user_input: User's message
        
    Returns:
        Detected ModuleType
        
    Usage:
        intent = quick_detect("what is sql join")
        # Returns: ModuleType.SQL_HELPER
    """
    detector = get_detector()
    return detector.detect(user_input)


# TODO: Future enhancements
# - Implement ML-based intent detection (scikit-learn, transformers)
# - Add context awareness (remember previous intents)
# - Support multi-intent detection (one input, multiple modules)
# - Add intent clarification (ask user if confidence is low)
# - Implement active learning (improve from user feedback)
# - Add support for custom user-trained models
