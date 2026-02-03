from .games import router as games_router
from .recommendations import router as recommendations_router
from .auth import router as auth_router

__all__ = [
    "games_router",
    "recommendations_router",
    "auth_router",
]
