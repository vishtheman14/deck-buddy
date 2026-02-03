from typing import List
from app.models import (
    Game,
    RecommendationRequest,
    GameRecommendation,
    RecommendationResponse,
)
import logging
import random

logger = logging.getLogger(__name__)

class AIRecommendationService:
    """
    Service for generating AI-powered game recommendations.
    
    TODO: Implement LangGraph workflow for intelligent recommendations.
    Currently uses simple mock logic.
    """
    
    def __init__(self):
        # Initialize LLM client here (Anthropic, OpenAI, etc.)
        pass
    
    def generate_recommendation(
        self,
        request: RecommendationRequest,
        games: List[Game]
    ) -> RecommendationResponse:
        """
        Generate a game recommendation based on user's current state.
        
        Args:
            request: User's mood, time, and energy preferences
            games: List of games in user's library
            
        Returns:
            Recommendation with reasoning
        """
        
        # TODO: Replace this with actual LangGraph logic
        # This is just a placeholder that returns a random game
        
        if not games:
            raise ValueError("User has no games in library")
        
        # Mock recommendation logic
        recommended_game = random.choice(games)
        alternatives = random.sample(games, min(3, len(games) - 1))
        
        recommendation = GameRecommendation(
            game=recommended_game,
            match_score=random.randint(75, 98),
            reasoning=self._generate_mock_reasoning(request, recommended_game),
            estimated_session_time=request.time_available
        )
        
        alternative_recommendations = [
            GameRecommendation(
                game=game,
                match_score=random.randint(60, 85),
                reasoning=f"Alternative match based on your preferences",
                estimated_session_time=request.time_available
            )
            for game in alternatives
        ]
        
        return RecommendationResponse(
            recommendation=recommendation,
            alternatives=alternative_recommendations
        )
    
    def _generate_mock_reasoning(self, request: RecommendationRequest, game: Game) -> str:
        """Generate mock reasoning (to be replaced with LLM-generated reasoning)"""
        
        mood_phrases = {
            "chill": "perfect for a relaxed gaming session",
            "focused": "great for focused, immersive gameplay",
            "social": "excellent for multiplayer and social interaction",
            "competitive": "ideal for competitive play",
            "story": "offers an engaging narrative experience"
        }
        
        energy_phrases = {
            "low": "doesn't require intense concentration",
            "medium": "provides engaging but manageable gameplay",
            "high": "matches your high energy level with fast-paced action"
        }
        
        mood_reason = mood_phrases.get(request.mood, "suits your mood")
        energy_reason = energy_phrases.get(request.energy_level, "fits your energy level")
        
        return f"{game.name} is {mood_reason} and {energy_reason}. With {request.time_available} minutes available, you can have a satisfying session."

# Create a singleton instance
ai_service = AIRecommendationService()
