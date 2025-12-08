"""
Hugging Face Zero-Shot Classification service.
Integrates with facebook/bart-large-mnli model via Inference API.
"""
import httpx
from typing import Dict, List, Optional
from loguru import logger
from config import get_settings

settings = get_settings()


class HuggingFaceService:
    """Service for Hugging Face zero-shot classification."""
    
    def __init__(self):
        self.api_url = f"{settings.huggingface_api_url}/{settings.huggingface_model}"
        self.headers = {
            "Authorization": f"Bearer {settings.huggingface_api_token}"
        }
        self.timeout = settings.huggingface_timeout
    
    async def classify(self, text: str, candidate_labels: List[str]) -> Dict[str, any]:
        """
        Classify text using zero-shot classification.
        
        Args:
            text: Text to classify
            candidate_labels: List of possible categories
            
        Returns:
            Dictionary with 'category' and 'score' keys
            
        Raises:
            Exception: If API call fails or returns invalid response
        """
        payload = {
            "inputs": text,
            "parameters": {
                "candidate_labels": candidate_labels
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Calling Hugging Face API for classification")
                logger.info(f"API URL: {self.api_url}")
                logger.info(f"Token: {self.headers['Authorization'][:15]}...")
                
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                # Check for errors
                if response.status_code == 503:
                    raise Exception("Hugging Face model is loading. Please try again in a few moments.")
                
                if response.status_code == 401:
                    raise Exception("Invalid Hugging Face API token")
                
                if response.status_code != 200:
                    logger.error(f"HF API error: {response.status_code} - {response.text}")
                    raise Exception(f"Hugging Face API error: {response.status_code} at {self.api_url}")
                
                result = response.json()
                logger.info(f"HF API Response: {result}")
                
                # Handle different response formats
                if isinstance(result, list):
                    result = result[0]
                
                # Extract top prediction
                if "labels" in result and "scores" in result:
                    category = result["labels"][0]
                    score = result["scores"][0]
                elif "label" in result and "score" in result:
                    category = result["label"]
                    score = result["score"]
                else:
                    raise Exception(f"Invalid response format from Hugging Face API: {result}")
                
                logger.info(f"Classification result: {category} (score: {score:.3f})")
                
                return {
                    "category": category,
                    "score": float(score)
                }
                
        except httpx.TimeoutException:
            logger.error("Hugging Face API timeout")
            raise Exception("Hugging Face API request timed out")
        
        except httpx.RequestError as e:
            logger.error(f"Hugging Face API request error: {str(e)}")
            raise Exception(f"Network error connecting to Hugging Face: {str(e)}")
        
        except Exception as e:
            logger.error(f"Hugging Face classification error: {str(e)}")
            raise


# Singleton instance
huggingface_service = HuggingFaceService()
