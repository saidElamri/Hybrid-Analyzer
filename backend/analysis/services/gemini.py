"""
Google Gemini API service for text summarization and tone detection.
Uses prompt engineering to generate structured responses.

NOTE: Currently using mock implementation due to Gemini API model access issues.
The real implementation is ready and can be activated once API access is resolved.
"""
import google.generativeai as genai
from typing import Dict
from loguru import logger
from config import get_settings
import re

settings = get_settings()

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)

# Mock mode flag - set to False when Gemini API access is resolved
# NOTE: Using production model
USE_MOCK = False


class GeminiService:
    """Service for Gemini API text analysis."""
    
    def __init__(self):
        if not USE_MOCK:
            model_name = 'gemini-2.5-flash'
            logger.info(f"Initializing Gemini Service with model: {model_name}")
            self.model = genai.GenerativeModel(model_name)
        self.timeout = settings.gemini_timeout
    
    def _build_prompt(self, text: str, category: str) -> str:
        """
        Build a contextualized prompt for Gemini.
        
        Args:
            text: Original text to analyze
            category: Predicted category from Hugging Face
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert text analyst. Analyze the following text that has been categorized as "{category}".

Your task:
1. Provide a concise summary (2-3 sentences, max 150 words)
2. Detect the overall tone: positive, neutral, or negative

Text to analyze:
{text}

Respond in this exact format:
SUMMARY: [your summary here]
TONE: [positive/neutral/negative]

Be precise and follow the format exactly."""
        
        return prompt
    
    async def analyze(self, text: str, category: str) -> Dict[str, str]:
        """
        Generate summary and detect tone using Gemini API.
        
        Args:
            text: Text to analyze
            category: Predicted category from classification
            
        Returns:
            Dictionary with 'summary' and 'tone' keys
            
        Raises:
            Exception: If API call fails or response is malformed
        """
        if USE_MOCK:
            return self._mock_analyze(text, category)
        
        try:
            logger.info(f"Calling Gemini API for analysis")
            
            prompt = self._build_prompt(text, category)
            
            # Generate content
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("Empty response from Gemini API")
            
            result_text = response.text.strip()
            logger.debug(f"Gemini response: {result_text}")
            
            # Parse response
            summary_match = re.search(r'SUMMARY:\s*(.+?)(?=TONE:|$)', result_text, re.DOTALL | re.IGNORECASE)
            tone_match = re.search(r'TONE:\s*(positive|neutral|negative)', result_text, re.IGNORECASE)
            
            if not summary_match or not tone_match:
                logger.warning("Failed to parse Gemini response, using fallback")
                # Fallback: use entire response as summary and detect tone from keywords
                summary = result_text[:500]
                tone = self._detect_tone_fallback(result_text)
            else:
                summary = summary_match.group(1).strip()
                tone = tone_match.group(1).lower()
            
            logger.info(f"Analysis complete: tone={tone}")
            
            return {
                "summary": summary,
                "tone": tone
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            
            # Provide fallback response
            if "API_KEY" in str(e).upper():
                raise Exception("Invalid Gemini API key")
            
            raise Exception(f"Gemini API error: {str(e)}")
    
    def _mock_analyze(self, text: str, category: str) -> Dict[str, str]:
        """
        Mock implementation for demonstration purposes.
        Generates contextual summary and tone based on the text and category.
        
        Args:
            text: Text to analyze
            category: Predicted category from classification
            
        Returns:
            Dictionary with 'summary' and 'tone' keys
        """
        logger.info(f"Using MOCK Gemini analysis (category: {category})")
        
        # Generate contextual summary based on category
        text_preview = text[:100] + "..." if len(text) > 100 else text
        
        summary = f"This {category.lower()}-related content discusses: {text_preview} "
        summary += f"The analysis indicates this is primarily focused on {category.lower()} matters with relevant insights and implications."
        
        # Detect tone from keywords
        tone = self._detect_tone_fallback(text)
        
        logger.info(f"Mock analysis complete: tone={tone}")
        
        return {
            "summary": summary,
            "tone": tone
        }
    
    def _detect_tone_fallback(self, text: str) -> str:
        """
        Fallback tone detection using keyword matching.
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected tone: positive, neutral, or negative
        """
        text_lower = text.lower()
        
        positive_keywords = ['good', 'great', 'excellent', 'positive', 'success', 'improve', 'benefit', 
                           'optimistic', 'growth', 'strong', 'high', 'gains', 'profit']
        negative_keywords = ['bad', 'poor', 'negative', 'fail', 'problem', 'issue', 'concern',
                           'decline', 'loss', 'weak', 'crisis', 'risk']
        
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"


# Singleton instance
gemini_service = GeminiService()
