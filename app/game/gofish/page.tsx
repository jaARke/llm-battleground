'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import fastApiClient from '@/lib/fastApiClient'

interface GameState {
  state: Record<string, any>
}

export default function GoFishPage() {
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Try to fetch existing game state first
    fetchGameState()
  }, [])

  const createGame = async () => {
    setLoading(true)
    setError(null)
    try {
      await fastApiClient.get('/game/gofish/create')
      // Fetch the new game state after creation
      await fetchGameStateInternal()
    } catch (err: any) {
      const errorMessage = typeof err.response?.data?.detail === 'string' 
        ? err.response.data.detail 
        : err.response?.data?.detail?.[0]?.msg || err.message || 'Failed to create game'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const fetchGameStateInternal = async () => {
    try {
      const response = await fastApiClient.get('/game/gofish/state')
      setGameState(response.data)
    } catch (err: any) {
      // Silently fail for internal calls (like after create)
      setGameState(null)
    }
  }

  const fetchGameState = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fastApiClient.get('/game/gofish/state')
      setGameState(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch game state')
      setGameState(null)
    } finally {
      setLoading(false)
    }
  }

  const endGame = async () => {
    setLoading(true)
    setError(null)
    try {
      await fastApiClient.get('/game/gofish/end')
      setGameState(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to end game')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen gradient-bg-primary flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-4xl w-full space-y-6">
        <h1 className="text-4xl font-bold text-center mb-8">Go Fish</h1>
        
        <div className="flex flex-col items-center space-y-4">
          <div className="flex space-x-4">
            <Button 
              onClick={gameState ? endGame : createGame} 
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {loading ? gameState ? 'Ending...' : 'Creating...' : gameState ? 'End Game' : 'Create Game'}
            </Button>
            <Button 
              onClick={fetchGameState} 
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {loading ? 'Loading...' : 'Refresh State'}
            </Button>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded max-w-lg">
              {error}
            </div>
          )}

          {gameState && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded max-w-lg">
              Game Active
            </div>
          )}
        </div>

        {gameState && (
          <div className="mt-8">
            <h2 className="text-2xl font-semibold mb-4 text-center">Game State</h2>
            <div className="bg-gray-800 text-green-400 p-6 rounded-lg overflow-auto max-h-96">
              <pre className="whitespace-pre-wrap text-sm">
                {JSON.stringify(gameState, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
