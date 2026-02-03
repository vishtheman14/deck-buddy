// API service for communicating with the FastAPI backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types matching our backend models
export interface Game {
  appid: number;
  name: string;
  playtime_forever: number;
  playtime_2weeks?: number;
  img_icon_url?: string;
  img_logo_url?: string;
}

export interface GameLibrary {
  game_count: number;
  games: Game[];
}

export interface RecommendationRequest {
  steam_id: string;
  mood: 'chill' | 'focused' | 'social' | 'competitive' | 'story';
  time_available: number;
  energy_level: 'low' | 'medium' | 'high';
}

export interface GameRecommendation {
  game: Game;
  match_score: number;
  reasoning: string;
  estimated_session_time: number;
}

export interface RecommendationResponse {
  recommendation: GameRecommendation;
  alternatives: GameRecommendation[];
}

/**
 * Fetch a user's Steam library
 */
export async function fetchUserLibrary(steamId: string): Promise<GameLibrary> {
  const response = await fetch(`${API_BASE_URL}/games/library/${steamId}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch library: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Generate an AI-powered game recommendation
 */
export async function generateRecommendation(
  request: RecommendationRequest
): Promise<RecommendationResponse> {
  const response = await fetch(`${API_BASE_URL}/recommendations/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to generate recommendation: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Get detailed information about a specific game
 */
export async function fetchGameDetails(appId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/games/details/${appId}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch game details: ${response.statusText}`);
  }
  
  return response.json();
}