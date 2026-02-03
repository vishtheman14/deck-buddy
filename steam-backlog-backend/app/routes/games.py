from fastapi import APIRouter, HTTPException, Query
from app.models import GameLibraryResponse
from app.services import steam_api
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/library/{steam_id}", response_model=GameLibraryResponse)
async def get_user_library(
    steam_id: str,
    include_appinfo: bool = Query(True, description="Include game names and metadata")
):
    """
    Fetch all games owned by a Steam user.
    
    Args:
        steam_id: User's 64-bit Steam ID
        include_appinfo: Whether to include game metadata
        
    Returns:
        List of games with playtime and other info
        
    Example:
        GET /games/library/76561197960435530
    """
    logger.info(f"Fetching library for Steam ID: {steam_id}")
    
    library = steam_api.get_owned_games(steam_id, include_appinfo=include_appinfo)
    
    if library is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch games from Steam API. Check if Steam ID is valid and profile is public."
        )
    
    if library.game_count == 0:
        raise HTTPException(
            status_code=404,
            detail="No games found. User profile might be private or they own no games."
        )
    
    logger.info(f"Successfully fetched {library.game_count} games")
    return library

@router.get("/details/{app_id}")
async def get_game_details(app_id: int):
    """
    Get detailed information about a specific game.
    
    Args:
        app_id: Steam application ID
        
    Returns:
        Game details from Steam Store API
        
    Example:
        GET /games/details/730  (Counter-Strike 2)
    """
    logger.info(f"Fetching details for app ID: {app_id}")
    
    details = steam_api.get_game_details(app_id)
    
    if details is None:
        raise HTTPException(
            status_code=404,
            detail=f"Game not found or details unavailable for app ID: {app_id}"
        )
    
    return details
