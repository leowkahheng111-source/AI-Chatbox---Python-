"""
Tests for router module.

Run: pytest tests/test_router.py
"""

import pytest
from backend.router import Router
from config.constants import ModuleType
from modules.calculator.calculator_service import CalculatorService


def test_router_initialization():
    """Test router initializes correctly."""
    router = Router()
    assert router is not None
    assert len(router.modules) == 0


def test_module_registration():
    """Test module registration."""
    router = Router()
    calculator = CalculatorService()
    
    router.register_module(ModuleType.CALCULATOR, calculator)
    assert ModuleType.CALCULATOR in router.modules


def test_route_calculator():
    """Test routing to calculator module."""
    router = Router()
    calculator = CalculatorService()
    router.register_module(ModuleType.CALCULATOR, calculator)
    
    response = router.route("Calculate 2 + 2")
    assert response is not None
    assert "4" in response["content"]


# TODO: Add more tests
# - Test all module types
# - Test error handling
# - Test module unavailability
# - Test response formatting
