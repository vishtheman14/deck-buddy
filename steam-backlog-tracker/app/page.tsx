'use client'

import { useState, useEffect } from 'react'
import { Sparkles, Clock, Zap, Smile, Gamepad2, Loader2 } from 'lucide-react'
import { fetchUserLibrary, generateRecommendation, type Game, type GameRecommendation } from '@/lib/api'

// Hardcoded Steam ID for now (we'll add proper auth later)
const STEAM_ID = '76561198047666747'

const moods = [
  { value: 'chill', label: 'Chill & Relaxed', emoji: '😌' },
  { value: 'focused', label: 'Focused', emoji: '🎯' },
  { value: 'social', label: 'Social', emoji: '👥' },
  { value: 'competitive', label: 'Competitive', emoji: '🏆' },
  { value: 'story', label: 'Story-driven', emoji: '📖' },
]

const timeSlots = [
  { value: '15', label: '15 min' },
  { value: '30', label: '30 min' },
  { value: '60', label: '1 hour' },
  { value: '120', label: '2+ hours' },
]

const energyLevels = [
  { value: 'low', label: 'Low Energy', emoji: '😴' },
  { value: 'medium', label: 'Medium', emoji: '😐' },
  { value: 'high', label: 'High Energy', emoji: '⚡' },
]

export default function LibraryPage() {
  const [mood, setMood] = useState('focused')
  const [time, setTime] = useState('60')
  const [energy, setEnergy] = useState('medium')
  
  // Real data from API
  const [games, setGames] = useState<Game[]>([])
  const [recommendation, setRecommendation] = useState<GameRecommendation | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch user's library on mount
  useEffect(() => {
    async function loadLibrary() {
      try {
        setLoading(true)
        const library = await fetchUserLibrary(STEAM_ID)
        setGames(library.games)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load library')
      } finally {
        setLoading(false)
      }
    }
    
    loadLibrary()
  }, [])

  // Generate recommendation when preferences change
  useEffect(() => {
    async function getRecommendation() {
      if (games.length === 0) return
      
      try {
        const result = await generateRecommendation({
          steam_id: STEAM_ID,
          mood: mood as any,
          time_available: parseInt(time),
          energy_level: energy as any,
        })
        setRecommendation(result.recommendation)
      } catch (err) {
        console.error('Failed to generate recommendation:', err)
      }
    }
    
    getRecommendation()
  }, [mood, time, energy, games])

  // Helper to get game image URL
  const getGameImage = (game: Game) => {
    if (game.img_logo_url) {
      return `https://cdn.akamai.steamstatic.com/steam/apps/${game.appid}/${game.img_logo_url}.jpg`
    }
    return `https://cdn.akamai.steamstatic.com/steam/apps/${game.appid}/header.jpg`
  }

  // Helper to convert playtime from minutes to hours
  const getPlaytimeHours = (minutes: number) => {
    return Math.round(minutes / 60)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-steam-lightblue animate-spin mx-auto mb-4" />
          <p className="text-xl text-gray-300">Loading your Steam library...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-effect rounded-xl p-8 max-w-md text-center">
          <p className="text-xl text-red-400 mb-4">Error loading library</p>
          <p className="text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <Gamepad2 className="w-8 h-8 text-steam-lightblue" />
            <h1 className="text-3xl font-bold text-white">Your Library</h1>
          </div>
          <button className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-white font-medium transition-colors">
            Logout
          </button>
        </div>

        {/* Controls Panel */}
        <div className="glass-effect rounded-xl p-6 mb-8">
          <div className="flex items-center gap-2 mb-6">
            <Sparkles className="w-5 h-5 text-steam-lightblue" />
            <h2 className="text-xl font-semibold text-white">What are you in the mood for?</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Mood Selector */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium mb-3 text-gray-300">
                <Smile className="w-4 h-4" />
                Mood
              </label>
              <div className="space-y-2">
                {moods.map((m) => (
                  <button
                    key={m.value}
                    onClick={() => setMood(m.value)}
                    className={`w-full px-4 py-3 rounded-lg text-left transition-all ${
                      mood === m.value
                        ? 'bg-steam-lightblue text-white font-medium'
                        : 'bg-steam-dark hover:bg-opacity-80 text-gray-300'
                    }`}
                  >
                    <span className="mr-2">{m.emoji}</span>
                    {m.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Time Selector */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium mb-3 text-gray-300">
                <Clock className="w-4 h-4" />
                Time Available
              </label>
              <div className="grid grid-cols-2 gap-2">
                {timeSlots.map((t) => (
                  <button
                    key={t.value}
                    onClick={() => setTime(t.value)}
                    className={`px-4 py-3 rounded-lg transition-all ${
                      time === t.value
                        ? 'bg-steam-lightblue text-white font-medium'
                        : 'bg-steam-dark hover:bg-opacity-80 text-gray-300'
                    }`}
                  >
                    {t.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Energy Selector */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium mb-3 text-gray-300">
                <Zap className="w-4 h-4" />
                Energy Level
              </label>
              <div className="space-y-2">
                {energyLevels.map((e) => (
                  <button
                    key={e.value}
                    onClick={() => setEnergy(e.value)}
                    className={`w-full px-4 py-3 rounded-lg text-left transition-all ${
                      energy === e.value
                        ? 'bg-steam-lightblue text-white font-medium'
                        : 'bg-steam-dark hover:bg-opacity-80 text-gray-300'
                    }`}
                  >
                    <span className="mr-2">{e.emoji}</span>
                    {e.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Recommended Game - Featured */}
        {recommendation && (
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-yellow-400" />
              <h2 className="text-2xl font-bold text-white">Perfect Match for You</h2>
            </div>
            
            <div className="relative glass-effect rounded-xl overflow-hidden game-card-hover cursor-pointer group">
              <div className="absolute top-4 right-4 bg-yellow-400 text-steam-dark px-4 py-2 rounded-full font-bold text-lg z-10">
                {recommendation.match_score}% Match
              </div>
              
              <div className="grid md:grid-cols-2 gap-6 p-6">
                <div className="relative aspect-video rounded-lg overflow-hidden">
                  <img
                    src={getGameImage(recommendation.game)}
                    alt={recommendation.game.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                
                <div className="flex flex-col justify-center">
                  <h3 className="text-3xl font-bold text-white mb-3">{recommendation.game.name}</h3>
                  <p className="text-gray-300 mb-4">{recommendation.reasoning}</p>
                  <p className="text-gray-400 mb-6">
                    {getPlaytimeHours(recommendation.game.playtime_forever)} hours played
                  </p>
                  <button className="w-full md:w-auto px-8 py-4 bg-steam-green hover:bg-opacity-80 text-white rounded-lg font-bold text-lg transition-all">
                    Play Now
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Other Games Library */}
        <div>
          <h2 className="text-xl font-semibold text-white mb-4">
            Your Library ({games.length} games)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {games.slice(0, 12).map((game) => (
              <div
                key={game.appid}
                className="glass-effect rounded-lg overflow-hidden game-card-hover cursor-pointer"
              >
                <div className="relative">
                  <img
                    src={getGameImage(game)}
                    alt={game.name}
                    className="w-full aspect-video object-cover"
                  />
                </div>
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-white mb-2 truncate">{game.name}</h3>
                  <p className="text-sm text-gray-500">{getPlaytimeHours(game.playtime_forever)}h played</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}