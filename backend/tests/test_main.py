"""
Tests for the main FastAPI application.
Run with: pytest backend/tests/
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "healthy"


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_generate_meme_success(client):
    """Test successful meme generation with mocked services."""
    # Mock the services
    with patch("main.OpenAIService") as mock_openai, \
         patch("main.ContentSafetyService") as mock_safety:
        
        # Setup mocks
        mock_openai_instance = AsyncMock()
        mock_openai_instance.generate_meme_text.return_value = {
            "text": "When you fix a bug\nBut create two more",
            "topic": "coding",
            "mood": "funny"
        }
        mock_openai_instance.generate_meme_suggestion.return_value = {
            "top_text": "WHEN YOU FIX A BUG",
            "bottom_text": "BUT CREATE TWO MORE"
        }
        
        mock_safety_instance = AsyncMock()
        mock_safety_instance.analyze_text.return_value = (True, {"is_safe": True})
        
        app.state.openai_service = mock_openai_instance
        app.state.content_safety_service = mock_safety_instance
        
        # Make request
        response = client.post(
            "/api/generate-meme",
            json={"topic": "coding", "mood": "funny"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["is_safe"] is True
        assert "meme_text" in data


def test_generate_meme_validation_error(client):
    """Test meme generation with invalid input."""
    response = client.post(
        "/api/generate-meme",
        json={"topic": ""}  # Empty topic should fail validation
    )
    assert response.status_code == 422  # Validation error


def test_feedback_endpoint(client):
    """Test the feedback submission endpoint."""
    response = client.post(
        "/api/feedback",
        json={
            "meme_text": "Test meme text",
            "reason": "inappropriate",
            "user_comment": "This is not suitable"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
