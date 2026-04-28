"""
Tests for Agentforce Vibes Agent
"""

import pytest
from agent import VibesAgent, AgentConfig


@pytest.fixture
def agent():
    """Create a test agent"""
    config = AgentConfig(name="Test Agent")
    return VibesAgent(config)


def test_agent_initialization(agent):
    """Test agent initialization"""
    assert agent.config.name == "Test Agent"
    assert agent.config.version == "1.0.0"


def test_health_check(agent):
    """Test health check endpoint"""
    health = agent.health_check()
    assert health["status"] == "healthy"
    assert health["agent"] == "Test Agent"


def test_process_message(agent):
    """Test message processing"""
    result = agent.process_message("Hello Agent")
    assert result["status"] == "success"
    assert "Hello Agent" in result["message"]
