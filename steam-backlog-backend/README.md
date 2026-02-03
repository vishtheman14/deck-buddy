# Steam Backlog Tracker - Backend API

FastAPI backend for AI-powered game recommendations from Steam libraries.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── models/              # Pydantic schemas
│   │   ├── __init__.py
│   │   └── schemas.py       # Request/response models
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Steam OAuth (TODO)
│   │   ├── games.py         # Game library endpoints
│   │   └── recommendations.py  # AI recommendation endpoint
│   └── services/            # Business logic
│       ├── __init__.py
│       ├── steam_api.py     # Steam Web API client
│       └── ai_service.py    # AI recommendation service
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Make sure you're in the backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Steam API Key

1. Go to https://steamcommunity.com/dev/apikey
2. Sign in with your Steam account
3. Register for an API key
4. Copy your key

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Steam API key
# You need at minimum:
STEAM_API_KEY=your_actual_steam_api_key_here
```

### 5. Run the Server

```bash
# From the backend directory
cd app
python main.py

# Or use uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Games
- `GET /games/library/{steam_id}` - Fetch user's game library
- `GET /games/details/{app_id}` - Get game details

### Recommendations
- `POST /recommendations/generate` - Generate AI game recommendation

### Authentication (TODO)
- `GET /auth/steam/login` - Initiate Steam login
- `GET /auth/steam/callback` - Handle Steam OAuth callback
- `GET /auth/logout` - Logout

## Testing the API

### 1. Test with Steam ID

You can test without OAuth by using a Steam ID directly. Here's a public profile for testing:

**Gabe Newell's Steam ID**: `76561197960287930`

### 2. Get a User's Library

```bash
curl http://localhost:8000/games/library/76561197960287930
```

### 3. Generate a Recommendation

```bash
curl -X POST http://localhost:8000/recommendations/generate \
  -H "Content-Type: application/json" \
  -d '{
    "steam_id": "76561197960287930",
    "mood": "chill",
    "time_available": 60,
    "energy_level": "medium"
  }'
```

### 4. Interactive API Docs

Visit http://localhost:8000/docs to use the interactive Swagger UI where you can test all endpoints visually.

## Current Status

✅ **Implemented:**
- FastAPI server with CORS
- Steam API integration (get games, get player info)
- Request/response models with validation
- Game library endpoint
- Mock recommendation endpoint (returns random games with scores)
- Interactive API documentation

🚧 **TODO:**
- Steam OAuth implementation
- LangGraph AI recommendation workflow
- Database integration (PostgreSQL/Supabase)
- Recommendation history tracking
- User preference learning
- Game metadata caching
- Rate limiting

## Development Tips

### Hot Reload
The server runs with `--reload` by default, so it will automatically restart when you make code changes.

### Logging
All requests and errors are logged. Check your console output for debugging.

### API Documentation
FastAPI automatically generates:
- **Swagger UI** at `/docs` - Interactive testing interface
- **ReDoc** at `/redoc` - Beautiful documentation

## Next Steps

1. **Test the current API** with a real Steam ID
2. **Implement Steam OAuth** for actual login flow
3. **Replace mock AI service** with LangGraph workflow
4. **Connect frontend** to these endpoints
5. **Add database** for caching and history

## Common Issues

**Problem**: `ModuleNotFoundError: No module named 'app'`
**Solution**: Make sure you're running from the correct directory or use `python -m app.main`

**Problem**: `pydantic_core._pydantic_core.ValidationError` on settings
**Solution**: Make sure your `.env` file exists and has `STEAM_API_KEY` set

**Problem**: Steam API returns 403 Forbidden
**Solution**: Your API key might be invalid. Double-check it at https://steamcommunity.com/dev/apikey
