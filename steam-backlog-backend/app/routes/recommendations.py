from fastapi import APIRouter, HTTPException
from app.models import RecommendationRequest, RecommendationResponse
from app.services import steam_api, ai_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendation(request: RecommendationRequest):
    """
    Generate an AI-powered game recommendation based on user's current state.
    
    Args:
        request: Contains steam_id, mood, time_available, and energy_level
        
    Returns:
        Game recommendation with reasoning and match score
        
    Example request body:
        {
            "steam_id": "76561197960435530",
            "mood": "chill",
            "time_available": 60,
            "energy_level": "medium"
        }
    """
    logger.info(f"Generating recommendation for Steam ID: {request.steam_id}")
    logger.info(f"Parameters - Mood: {request.mood}, Time: {request.time_available}min, Energy: {request.energy_level}")
    
    # Fetch user's game library
    library = steam_api.get_owned_games(request.steam_id, include_appinfo=True)
    
    if library is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user's game library from Steam API"
        )
    
    if library.game_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User has no games in their library"
        )
    
    # Generate AI recommendation
    try:
        recommendation = ai_service.generate_recommendation(request, library.games)
        logger.info(f"Successfully generated recommendation: {recommendation.recommendation.game.name}")
        return recommendation
        
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendation: {str(e)}"
        )
