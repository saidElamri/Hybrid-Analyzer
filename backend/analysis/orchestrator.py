"""
Orchestrator for coordinating Hugging Face and Gemini services.
Manages the complete analysis workflow.
"""
from typing import Dict
from loguru import logger
from analysis.services.huggingface import huggingface_service
from analysis.services.gemini import gemini_service


class AnalysisOrchestrator:
    """Orchestrates the analysis workflow between HF and Gemini."""
    
    async def analyze(self, text: str, candidate_labels: list) -> Dict[str, any]:
        """
        Perform complete analysis workflow.
        
        Workflow:
        1. Classify text using Hugging Face
        2. Send category + text to Gemini for summary and tone
        3. Aggregate results
        
        Args:
            text: Text to analyze
            candidate_labels: Categories for classification
            
        Returns:
            Dictionary with category, score, summary, and tone
            
        Raises:
            Exception: If any step fails
        """
        logger.info("Starting analysis orchestration")
        
        try:
            # Step 1: Classify with Hugging Face
            logger.info("Step 1: Classifying with Hugging Face")
            classification_result = await huggingface_service.classify(text, candidate_labels)
            
            category = classification_result["category"]
            score = classification_result["score"]
            
            logger.info(f"Classification complete: {category} ({score:.3f})")
            
            # Step 2: Analyze with Gemini
            logger.info("Step 2: Analyzing with Gemini")
            gemini_result = await gemini_service.analyze(text, category)
            
            summary = gemini_result["summary"]
            tone = gemini_result["tone"]
            
            logger.info(f"Gemini analysis complete: tone={tone}")
            
            # Step 3: Aggregate results
            result = {
                "category": category,
                "score": score,
                "summary": summary,
                "tone": tone
            }
            
            logger.info("Analysis orchestration complete")
            return result
            
        except Exception as e:
            logger.error(f"Analysis orchestration failed: {str(e)}")
            raise


# Singleton instance
orchestrator = AnalysisOrchestrator()
