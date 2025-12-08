"""
Analysis routes for text analysis endpoint.
Protected by JWT authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from database import get_db
from auth.models import User, AnalysisLog
from auth.middleware import get_current_user
from analysis.schemas import AnalyzeRequest, AnalyzeResponse
from analysis.orchestrator import orchestrator

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("", response_model=AnalyzeResponse)
async def analyze_text(
    request: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze text using Hugging Face and Gemini APIs.
    
    This endpoint:
    1. Classifies text using Hugging Face zero-shot classification
    2. Generates summary and detects tone using Gemini API
    3. Returns aggregated results
    4. Logs analysis to database
    
    Args:
        request: Analysis request with text and optional candidate labels
        current_user: Authenticated user (injected by middleware)
        db: Database session
        
    Returns:
        Analysis results with category, score, summary, and tone
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        logger.info(f"Analysis request from user {current_user.username}")
        
        # Perform analysis
        result = await orchestrator.analyze(
            text=request.text,
            candidate_labels=request.candidate_labels
        )
        
        # Log analysis to database
        analysis_log = AnalysisLog(
            user_id=current_user.id,
            input_text=request.text[:1000],  # Store first 1000 chars
            category=result["category"],
            confidence_score=result["score"],
            summary=result["summary"],
            tone=result["tone"]
        )
        
        db.add(analysis_log)
        db.commit()
        
        logger.info(f"Analysis complete and logged (ID: {analysis_log.id})")
        
        return AnalyzeResponse(**result)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
