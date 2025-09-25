'use client'

import { useState } from 'react'
import ProtectedRoute from '@/components/ProtectedRoute'
import fastApiClient from '@/lib/fastApiClient'

type ProtectedResponse = {
  message: string
  user: {
    user_id: string
    username: string
    email: string
  }
  timestamp: string
}

export default function Home() {
  const [isTesting, setIsTesting] = useState(false)
  const [result, setResult] = useState<ProtectedResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const testProtectedEndpoint = async () => {
    setIsTesting(true)
    setError(null)
    setResult(null)

    try {
      const response = await fastApiClient.get<ProtectedResponse>('/protected')
      setResult(response.data)
    } catch (err: unknown) {
      console.error('Protected endpoint error:', err)
      setError('Unable to reach the protected endpoint. Please try again later.')
    } finally {
      setIsTesting(false)
    }
  }

  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-3xl mx-auto bg-white/85 dark:bg-gray-900/85 backdrop-blur rounded-3xl shadow-xl border border-gray-200/70 dark:border-gray-800/70 p-10 md:p-14 space-y-10">
          <header className="space-y-4 text-center">
            <p className="text-sm uppercase tracking-[0.35em] text-blue-500 dark:text-blue-400">
              LLM Battleground
            </p>
            <h1 className="text-4xl font-semibold text-gray-900 dark:text-gray-100">
              Welcome to the operations hub
            </h1>
            <p className="text-base md:text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Launch a quick systems check to confirm your access to protected LLM battle
              services.
            </p>
          </header>

          <div className="space-y-6">
            <button
              type="button"
              onClick={testProtectedEndpoint}
              disabled={isTesting}
              className="relative w-full flex items-center justify-center gap-3 rounded-2xl px-6 py-4 text-base font-semibold tracking-wide text-white transition bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-600 hover:to-purple-500 disabled:opacity-70 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
            >
              {isTesting ? 'Running secure systems check…' : 'Test protected endpoint'}
            </button>

            {error && (
              <p className="text-sm text-center text-red-600 dark:text-red-400">{error}</p>
            )}

            {result && (
              <div className="bg-gray-900/90 text-gray-100 rounded-2xl p-6 space-y-2 shadow-inner border border-gray-800">
                <p className="text-sm uppercase tracking-widest text-blue-300">Protected response</p>
                <pre className="text-xs md:text-sm overflow-x-auto whitespace-pre-wrap">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      </main>
    </ProtectedRoute>
  )
}
