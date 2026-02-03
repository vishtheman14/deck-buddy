from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class MoodType(str, Enum):
    """User's current mood"""
    CHILL = "chill"
    FOCUSED = "focused"
    SOCIAL = "social"
    COMPETITIVE = "competitive"
    STORY = "story"

class EnergyLevel(str, Enum):
    """User's current energy level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Game(BaseModel):
    """Steam game model"""
    app_id: int = Field(..., alias="appid")
    name: str
    playtime_forever: int = Field(0, description="Total playtime in minutes")
    playtime_2weeks: Optional[int] = Field(None, description="Playtime in last 2 weeks (minutes)")
    img_icon_url: Optional[str] = None
    img_logo_url: Optional[str] = None
    has_community_visible_stats: Optional[bool] = None
    
    class Config:
        populate_by_name = True

class GameLibraryResponse(BaseModel):
    """Response containing user's game library"""
    game_count: int
    games: List[Game]

class RecommendationRequest(BaseModel):
    """Request for game recommendation"""
    steam_id: str = Field(..., description="User's Steam ID")
    mood: MoodType = Field(..., description="Current mood")
    time_available: int = Field(..., ge=1, le=480, description="Available time in minutes")
    energy_level: EnergyLevel = Field(..., description="Current energy level")

class GameRecommendation(BaseModel):
    """AI-generated game recommendation"""
    game: Game
    match_score: int = Field(..., ge=0, le=100, description="Match percentage")
    reasoning: str = Field(..., description="Why this game was recommended")
    estimated_session_time: int = Field(..., description="Estimated session time in minutes")

class RecommendationResponse(BaseModel):
    """Response containing game recommendation"""
    recommendation: GameRecommendation
    alternatives: List[GameRecommendation] = Field(default_factory=list, max_length=5)

class SteamAuthResponse(BaseModel):
    """Response after successful Steam authentication"""
    steam_id: str
    persona_name: Optional[str] = None
    avatar_url: Optional[str] = None
    profile_url: Optional[str] = None
