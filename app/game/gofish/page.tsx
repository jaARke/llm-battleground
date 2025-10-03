'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import fastApiClient from '@/lib/fastApiClient'

interface GameState {
  state: Record<string, any>
}

export default function GoFishPage() {
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [gameId, setGameId] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Create a new game on initial load
    createGame()
  }, [])

  useEffect(() => {
    // Fetch initial game state if gameId is present
    if (gameId) {
      fetchGameState()
    }
  }, [gameId])

  const createGame = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fastApiClient.get('/game/gofish/create')
      setGameId(response.data.game_id)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create game')
    } finally {
      setLoading(false)
    }
  }

  const fetchGameState = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fastApiClient.get('/game/gofish/state?game_id=' + gameId)
      setGameState(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch game state')
    } finally {
      setLoading(false)
    }
  }

  const endGame = async () => {
    setLoading(true)
    setError(null)
    try {
      await fastApiClient.get('/game/gofish/end')
      setGameId(null)
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
              onClick={gameId ? endGame : createGame} 
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {loading ? gameId ? 'Ending...' : 'Creating...' : gameId ? 'End Game' : 'Create Game'}
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

          {gameId && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded max-w-lg">
              Game ID: {gameId}
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
