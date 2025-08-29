"""Tests for the langgraph_flow module."""

import pytest
from unittest.mock import patch, AsyncMock
from flows.langgraph_flow import FlowState, needs_retry, router, execute_code


class TestFlowState:
    """Test the FlowState dataclass."""
    
    def test_flow_state_initialization(self):
        """Test that FlowState can be properly initialized."""
        state = FlowState(user_input="test input")
        assert state.user_input == "test input"
        assert state.generated_code is None
        assert state.reviewer_feedback is None
        assert state.docs_code is None
        assert state.orchestrator_decision is None
        assert state.approval_status is None


class TestRouter:
    """Test the router function."""
    
    def test_router_generate_decision(self):
        """Test router with GENERATE decision."""
        state = FlowState(user_input="test", orchestrator_decision="GENERATE")
        result = router(state)
        assert result == "code_generator"
    
    def test_router_review_decision(self):
        """Test router with REVIEW decision."""
        state = FlowState(user_input="test", orchestrator_decision="REVIEW")
        result = router(state)
        assert result == "code_reviewer"
    
    def test_router_document_decision(self):
        """Test router with DOCUMENT decision."""
        state = FlowState(user_input="test", orchestrator_decision="DOCUMENT")
        result = router(state)
        assert result == "documentation_agent"
    
    def test_router_fallback_decision(self):
        """Test router with unknown decision."""
        state = FlowState(user_input="test", orchestrator_decision="UNKNOWN")
        result = router(state)
        assert result == "fallback_agent"


class TestNeedsRetry:
    """Test the needs_retry function."""
    
    def test_needs_retry_with_error(self):
        """Test needs_retry returns True when feedback contains 'error'."""
        state = FlowState(user_input="test", reviewer_feedback="There is an error in the code")
        assert needs_retry(state) is True
    
    def test_needs_retry_with_fix(self):
        """Test needs_retry returns True when feedback contains 'fix'."""
        state = FlowState(user_input="test", reviewer_feedback="Please fix this issue")
        assert needs_retry(state) is True
    
    def test_needs_retry_no_issues(self):
        """Test needs_retry returns False when no issues found."""
        state = FlowState(user_input="test", reviewer_feedback="Code looks good")
        assert needs_retry(state) is False
    
    def test_needs_retry_no_feedback(self):
        """Test needs_retry returns False when no feedback."""
        state = FlowState(user_input="test", reviewer_feedback=None)
        assert needs_retry(state) is False


class TestExecuteCode:
    """Test the execute_code tool."""
    
    def test_execute_code_with_result(self):
        """Test execute_code with valid code that sets result variable."""
        code = "result = 2 + 2"
        result = execute_code(code)
        assert result == "4"
    
    def test_execute_code_no_result_variable(self):
        """Test execute_code with code that doesn't set result variable."""
        code = "x = 5"
        result = execute_code(code)
        assert result == "No result variable defined."
    
    def test_execute_code_with_error(self):
        """Test execute_code with invalid code."""
        code = "result = 1 / 0"
        result = execute_code(code)
        assert "Error:" in result


if __name__ == "__main__":
    pytest.main([__file__])
