'use client'

import { Gamepad2, LogIn } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const router = useRouter()

  const handleSteamLogin = () => {
    // In production, this would redirect to Steam OAuth
    // For now, just simulate login and go to library
    router.push('/library')
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="glass-effect rounded-2xl p-8 max-w-md w-full text-center">
        <div className="flex justify-center mb-6">
          <div className="bg-steam-lightblue p-4 rounded-full">
            <Gamepad2 className="w-12 h-12 text-white" />
          </div>
        </div>
        
        <h1 className="text-3xl font-bold text-white mb-2">
          Steam Backlog Tracker
        </h1>
        <p className="text-gray-400 mb-8">
          AI-powered game recommendations based on your mood, time, and energy level
        </p>

        <button
          onClick={handleSteamLogin}
          className="w-full flex items-center justify-center gap-3 px-6 py-4 bg-steam-darker hover:bg-opacity-80 text-white rounded-lg font-semibold transition-all border border-steam-lightblue border-opacity-30"
        >
          <LogIn className="w-5 h-5" />
          Sign in with Steam
        </button>

        <p className="text-sm text-gray-500 mt-6">
          We'll analyze your Steam library to give you personalized game recommendations
        </p>
      </div>
    </div>
  )
}
