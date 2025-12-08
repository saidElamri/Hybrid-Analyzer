"""
Tests for analysis endpoints and services.
"""
import pytest
from unittest.mock import patch, AsyncMock
from tests.mocks import MockHuggingFaceService, MockGeminiService, MockHuggingFaceServiceError


def test_analyze_unauthorized(client):
    """Test analysis endpoint without authentication."""
    response = client.post(
        "/analyze",
        json={"text": "This is a test article about technology."}
    )
    
    assert response.status_code == 403  # Forbidden


@patch('analysis.orchestrator.huggingface_service', new_callable=lambda: MockHuggingFaceService())
@patch('analysis.orchestrator.gemini_service', new_callable=lambda: MockGeminiService())
def test_analyze_success(mock_gemini, mock_hf, client, auth_headers):
    """Test successful analysis with mocked services."""
    response = client.post(
        "/analyze",
        headers=auth_headers,
        json={
            "text": "This is a test article about artificial intelligence and machine learning."
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "category" in data
    assert "score" in data
    assert "summary" in data
    assert "tone" in data
    
    assert data["category"] == "technology"
    assert data["score"] == 0.95
    assert data["tone"] in ["positive", "neutral", "negative"]


def test_analyze_short_text(client, auth_headers):
    """Test analysis with text that's too short."""
    response = client.post(
        "/analyze",
        headers=auth_headers,
        json={"text": "Short"}
    )
    
    assert response.status_code == 422  # Validation error


def test_analyze_custom_labels(client, auth_headers):
    """Test analysis with custom candidate labels."""
    with patch('analysis.orchestrator.huggingface_service', new_callable=lambda: MockHuggingFaceService()):
        with patch('analysis.orchestrator.gemini_service', new_callable=lambda: MockGeminiService()):
            response = client.post(
                "/analyze",
                headers=auth_headers,
                json={
                    "text": "This is a test article.",
                    "candidate_labels": ["custom1", "custom2", "custom3"]
                }
            )
            
            assert response.status_code == 200


@patch('analysis.orchestrator.huggingface_service', new_callable=lambda: MockHuggingFaceServiceError())
def test_analyze_hf_error(mock_hf, client, auth_headers):
    """Test analysis when Hugging Face service fails."""
    response = client.post(
        "/analyze",
        headers=auth_headers,
        json={"text": "This is a test article about technology."}
    )
    
    assert response.status_code == 500
    assert "failed" in response.json()["detail"].lower()


def test_analyze_invalid_token(client):
    """Test analysis with invalid JWT token."""
    response = client.post(
        "/analyze",
        headers={"Authorization": "Bearer invalid_token"},
        json={"text": "This is a test article."}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_orchestrator_workflow():
    """Test the orchestrator workflow with mocks."""
    from analysis.orchestrator import AnalysisOrchestrator
    
    orchestrator = AnalysisOrchestrator()
    
    # Mock the services
    with patch('analysis.orchestrator.huggingface_service', new_callable=lambda: MockHuggingFaceService()):
        with patch('analysis.orchestrator.gemini_service', new_callable=lambda: MockGeminiService()):
            result = await orchestrator.analyze(
                text="Test article about AI",
                candidate_labels=["technology", "science"]
            )
            
            assert result["category"] == "technology"
            assert result["score"] == 0.95
            assert "summary" in result
            assert result["tone"] == "positive"
