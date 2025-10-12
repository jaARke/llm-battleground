'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Slider } from '@/components/ui/slider'
import { Checkbox } from '@/components/ui/checkbox'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Separator } from '@/components/ui/separator'
import fastApiClient from '@/lib/fastApiClient'

interface AIModel {
  internal_name: string
  display_name: string
}

interface GoFishGameParams {
  num_rounds: number
  starting_fish: number
  regeneration_rate: number
  extinction_penalty: number
  plentiful_bonus: number
}

interface GameState {
  user_email: string
  start_time: string
  players: AIModel[]
  status: string
  params: GoFishGameParams
}

interface CreateGoFishGameRequest {
  players: AIModel[]
  params: GoFishGameParams
}

export default function GoFishPage() {
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [availableModels, setAvailableModels] = useState<AIModel[]>([])
  const [selectedPlayers, setSelectedPlayers] = useState<AIModel[]>([])
  const [gameParams, setGameParams] = useState<GoFishGameParams>({
    num_rounds: 25,
    starting_fish: 500,
    regeneration_rate: 1.1,
    extinction_penalty: 0.5,
    plentiful_bonus: 1.2
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showConfig, setShowConfig] = useState(false)
  const [initialCheckDone, setInitialCheckDone] = useState(false)

  useEffect(() => {
    // Check for existing game and fetch available models
    initializePage()
  }, [])

  const initializePage = async () => {
    setLoading(true)
    try {
      // Check if a game already exists
      await checkExistingGame()
      
      // Fetch available models for configuration
      await fetchAvailableModels()
    } finally {
      setLoading(false)
      setInitialCheckDone(true)
    }
  }

  const checkExistingGame = async () => {
    try {
      const response = await fastApiClient.get('/game/gofish/state')
      setGameState(response.data)
      setShowConfig(false)
    } catch (err: any) {
      // No existing game found, show configuration
      setGameState(null)
      setShowConfig(true)
    }
  }

  const fetchAvailableModels = async () => {
    try {
      const response = await fastApiClient.get('/game/available_models')
      setAvailableModels(response.data)
    } catch (err: any) {
      console.error('Failed to fetch available models:', err)
      setError('Failed to load available AI models')
    }
  }

  const createGame = async () => {
    if (selectedPlayers.length < 2 || selectedPlayers.length > 4) {
      setError('Please select 2-4 players')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const createRequest: CreateGoFishGameRequest = {
        players: selectedPlayers,
        params: gameParams
      }
      
      const response = await fastApiClient.post('/game/gofish/create', createRequest)
      setGameState(response.data)
      setShowConfig(false)
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
      setShowConfig(false)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch game state')
      setGameState(null)
      setShowConfig(true)
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
      setShowConfig(true)
      setSelectedPlayers([])
      setError(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to end game')
    } finally {
      setLoading(false)
    }
  }

  const togglePlayerSelection = (model: AIModel) => {
    setSelectedPlayers(prev => {
      const isSelected = prev.some(p => p.internal_name === model.internal_name)
      if (isSelected) {
        return prev.filter(p => p.internal_name !== model.internal_name)
      } else if (prev.length < 4) {
        return [...prev, model]
      }
      return prev
    })
  }

  const startNewGame = () => {
    setShowConfig(true)
    setSelectedPlayers([])
    setError(null)
    setGameParams({
      num_rounds: 25,
      starting_fish: 500,
      regeneration_rate: 1.1,
      extinction_penalty: 0.5,
      plentiful_bonus: 1.2
    })
  }

  if (!initialCheckDone) {
    return (
      <main className="min-h-screen gradient-bg-primary flex flex-col items-center justify-center px-6 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">Go Fish</h1>
          <div className="text-lg">Loading...</div>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen gradient-bg-primary flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-6xl w-full space-y-6">
        <h1 className="text-4xl font-bold text-center mb-8">Go Fish</h1>
        
        {error && (
          <Alert className="bg-red-100 border-red-400">
            <AlertDescription className="text-red-700">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {showConfig && !gameState && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-semibold mb-2">Configure New Game</h2>
              <p className="text-gray-600">Select AI players and configure game parameters</p>
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              {/* Player Selection */}
              <Card>
                <CardHeader>
                  <CardTitle>Select Players (2-4)</CardTitle>
                  <div className="text-sm text-gray-600">
                    Selected: {selectedPlayers.length}/4
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-2 max-h-96 overflow-y-auto">
                    {availableModels.map((model) => {
                      const isSelected = selectedPlayers.some(p => p.internal_name === model.internal_name)
                      const isDisabled = !isSelected && selectedPlayers.length >= 4
                      
                      return (
                        <div key={model.internal_name} className="flex items-center space-x-3 p-2 rounded hover:bg-gray-50">
                          <Checkbox
                            id={model.internal_name}
                            checked={isSelected}
                            disabled={isDisabled}
                            onCheckedChange={() => togglePlayerSelection(model)}
                          />
                          <Label 
                            htmlFor={model.internal_name}
                            className={`text-sm cursor-pointer flex-grow ${isDisabled ? 'text-gray-400' : ''}`}
                          >
                            {model.display_name}
                          </Label>
                        </div>
                      )
                    })}
                  </div>
                </CardContent>
              </Card>

              {/* Game Parameters */}
              <Card>
                <CardHeader>
                  <CardTitle>Game Parameters</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-3">
                    <Label htmlFor="num_rounds">Number of Rounds: {gameParams.num_rounds}</Label>
                    <Slider
                      id="num_rounds"
                      min={1}
                      max={50}
                      step={1}
                      value={[gameParams.num_rounds]}
                      onValueChange={(value) => setGameParams(prev => ({ ...prev, num_rounds: value[0] }))}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-3">
                    <Label htmlFor="starting_fish">Starting Fish: {gameParams.starting_fish}</Label>
                    <Slider
                      id="starting_fish"
                      min={100}
                      max={1000}
                      step={50}
                      value={[gameParams.starting_fish]}
                      onValueChange={(value) => setGameParams(prev => ({ ...prev, starting_fish: value[0] }))}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-3">
                    <Label htmlFor="regeneration_rate">Regeneration Rate: {gameParams.regeneration_rate.toFixed(2)}</Label>
                    <Slider
                      id="regeneration_rate"
                      min={1.0}
                      max={2.0}
                      step={0.1}
                      value={[gameParams.regeneration_rate]}
                      onValueChange={(value) => setGameParams(prev => ({ ...prev, regeneration_rate: value[0] }))}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-3">
                    <Label htmlFor="extinction_penalty">Extinction Penalty: {gameParams.extinction_penalty.toFixed(2)}</Label>
                    <Slider
                      id="extinction_penalty"
                      min={0.0}
                      max={1.0}
                      step={0.1}
                      value={[gameParams.extinction_penalty]}
                      onValueChange={(value) => setGameParams(prev => ({ ...prev, extinction_penalty: value[0] }))}
                      className="w-full"
                    />
                  </div>

                  <div className="space-y-3">
                    <Label htmlFor="plentiful_bonus">Plentiful Bonus: {gameParams.plentiful_bonus.toFixed(2)}</Label>
                    <Slider
                      id="plentiful_bonus"
                      min={1.0}
                      max={2.0}
                      step={0.1}
                      value={[gameParams.plentiful_bonus]}
                      onValueChange={(value) => setGameParams(prev => ({ ...prev, plentiful_bonus: value[0] }))}
                      className="w-full"
                    />
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="flex justify-center">
              <Button 
                onClick={createGame} 
                disabled={loading || selectedPlayers.length < 2 || selectedPlayers.length > 4}
                className="bg-blue-600 hover:bg-blue-700 px-8 py-2"
                size="lg"
              >
                {loading ? 'Creating Game...' : 'Create Game'}
              </Button>
            </div>
          </div>
        )}

        {gameState && (
          <div className="space-y-6">
            <div className="flex justify-center space-x-4">
              <Button 
                onClick={endGame} 
                disabled={loading}
                className="bg-red-600 hover:bg-red-700"
              >
                {loading ? 'Ending...' : 'End Game'}
              </Button>
              <Button 
                onClick={fetchGameState} 
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {loading ? 'Loading...' : 'Refresh State'}
              </Button>
              <Button 
                onClick={startNewGame} 
                disabled={loading}
                variant="outline"
              >
                Configure New Game
              </Button>
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              {/* Game Info */}
              <Card>
                <CardHeader>
                  <CardTitle>Game Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <Label className="font-semibold">Status:</Label>
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                      {gameState.status}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <Label className="font-semibold">Started:</Label>
                    <span className="text-sm text-gray-600">
                      {new Date(gameState.start_time).toLocaleString()}
                    </span>
                  </div>
                  <Separator />
                  <div>
                    <Label className="font-semibold block mb-3">Players:</Label>
                    <div className="space-y-2">
                      {gameState.players.map((player, index) => (
                        <div key={player.internal_name} className="flex items-center justify-between text-sm bg-gray-50 px-3 py-2 rounded">
                          <span className="font-medium">Player {index + 1}</span>
                          <span className="text-gray-600">{player.display_name}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Game Parameters */}
              <Card>
                <CardHeader>
                  <CardTitle>Game Parameters</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="flex justify-between">
                      <Label className="font-semibold">Rounds:</Label>
                      <span>{gameState.params.num_rounds}</span>
                    </div>
                    <div className="flex justify-between">
                      <Label className="font-semibold">Starting Fish:</Label>
                      <span>{gameState.params.starting_fish}</span>
                    </div>
                    <div className="flex justify-between">
                      <Label className="font-semibold">Regeneration:</Label>
                      <span>{gameState.params.regeneration_rate}x</span>
                    </div>
                    <div className="flex justify-between">
                      <Label className="font-semibold">Extinction Penalty:</Label>
                      <span>{gameState.params.extinction_penalty}x</span>
                    </div>
                    <div className="col-span-2 flex justify-between">
                      <Label className="font-semibold">Plentiful Bonus:</Label>
                      <span>{gameState.params.plentiful_bonus}x</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Full Game State */}
            <Card>
              <CardHeader>
                <CardTitle>Full Game State</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-800 text-green-400 p-6 rounded-lg overflow-auto max-h-96">
                  <pre className="whitespace-pre-wrap text-sm">
                    {JSON.stringify(gameState, null, 2)}
                  </pre>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </main>
  )
}
