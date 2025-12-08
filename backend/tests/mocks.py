"""
Mock responses for Hugging Face and Gemini APIs.
"""


class MockHuggingFaceResponse:
    """Mock Hugging Face API response."""
    
    def __init__(self, category="technology", score=0.95):
        self.status_code = 200
        self._json = {
            "labels": [category, "politics", "sports"],
            "scores": [score, 0.03, 0.02]
        }
    
    def json(self):
        return self._json


class MockGeminiResponse:
    """Mock Gemini API response."""
    
    def __init__(self, summary="This is a test summary.", tone="positive"):
        self.text = f"SUMMARY: {summary}\nTONE: {tone}"


class MockHuggingFaceService:
    """Mock Hugging Face service for testing."""
    
    async def classify(self, text, candidate_labels):
        """Mock classification."""
        return {
            "category": "technology",
            "score": 0.95
        }


class MockGeminiService:
    """Mock Gemini service for testing."""
    
    async def analyze(self, text, category):
        """Mock analysis."""
        return {
            "summary": "This is a test summary about technology.",
            "tone": "positive"
        }


class MockHuggingFaceServiceError:
    """Mock Hugging Face service that raises errors."""
    
    async def classify(self, text, candidate_labels):
        """Mock classification that fails."""
        raise Exception("Hugging Face API error")


class MockGeminiServiceError:
    """Mock Gemini service that raises errors."""
    
    async def analyze(self, text, category):
        """Mock analysis that fails."""
        raise Exception("Gemini API error")
