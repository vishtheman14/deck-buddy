import requests
from typing import Optional, List, Dict, Any
from app.config import settings
from app.models import Game, GameLibraryResponse
import logging

logger = logging.getLogger(__name__)

class SteamAPIService:
    """
    Service for interacting with Steam Web API.
    
    Documentation: https://partner.steamgames.com/doc/webapi_overview
    """
    
    BASE_URL = "http://api.steampowered.com"
    STORE_API_URL = "https://store.steampowered.com/api"
    
    def __init__(self):
        self.api_key = settings.steam_api_key
        
    def get_owned_games(self, steam_id: str, include_appinfo: bool = True) -> Optional[GameLibraryResponse]:
        """
        Fetch all games owned by a user.
        
        Args:
            steam_id: User's Steam ID (64-bit)
            include_appinfo: Include game name and other info
            
        Returns:
            GameLibraryResponse with list of games, or None if request fails
        """
        url = f"{self.BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
        
        params = {
            "key": self.api_key,
            "steamid": steam_id,
            "format": "json",
            "include_appinfo": include_appinfo,
            "include_played_free_games": True,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "response" not in data:
                logger.error(f"Unexpected response format: {data}")
                return None
                
            game_data = data["response"]
            
            if "games" not in game_data:
                # User might have private profile or no games
                logger.warning(f"No games found for Steam ID: {steam_id}")
                return GameLibraryResponse(game_count=0, games=[])
            
            games = [Game(**game) for game in game_data["games"]]
            
            return GameLibraryResponse(
                game_count=game_data.get("game_count", len(games)),
                games=games
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching games for {steam_id}: {str(e)}")
            return None
    
    def get_player_summaries(self, steam_ids: List[str]) -> Optional[List[Dict[str, Any]]]:
        """
        Get player profile information.
        
        Args:
            steam_ids: List of Steam IDs (up to 100)
            
        Returns:
            List of player summaries
        """
        url = f"{self.BASE_URL}/ISteamUser/GetPlayerSummaries/v0002/"
        
        params = {
            "key": self.api_key,
            "steamids": ",".join(steam_ids),
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("response", {}).get("players", [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching player summaries: {str(e)}")
            return None
    
    def get_game_details(self, app_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific game from Steam Store API.
        
        Note: This is a different API than the Steam Web API and doesn't require a key.
        
        Args:
            app_id: Steam application ID
            
        Returns:
            Game details dictionary
        """
        url = f"{self.STORE_API_URL}/appdetails"
        
        params = {
            "appids": app_id,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if str(app_id) in data and data[str(app_id)]["success"]:
                return data[str(app_id)]["data"]
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching game details for {app_id}: {str(e)}")
            return None

# Create a singleton instance
steam_api = SteamAPIService()
