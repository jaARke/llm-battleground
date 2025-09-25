'use client'

import { useState, useEffect } from 'react'
import AuthComponent from '../components/AuthComponent'

export default function Home() {
  const [displayText, setDisplayText] = useState('')
  const [showSubtext, setShowSubtext] = useState(false)
  const fullText = 'LLM Battleground'

  useEffect(() => {
    let index = 0
    const timer = setInterval(() => {
      if (index < fullText.length) {
        setDisplayText(fullText.slice(0, index + 1))
        index++
      } else {
        clearInterval(timer)
        // Show subtext after main text is complete
        setTimeout(() => setShowSubtext(true), 500)
      }
    }, 100) // 100ms delay between characters

    return () => clearInterval(timer)
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-start bg-gray-50 dark:bg-gray-900 p-4 pt-32">
      <div className="flex flex-col items-center space-y-8">
        {/* Construction emoji */}
        <div className="text-8xl">🚧</div>

        {/* Main title with typewriter effect */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-100">
            {displayText}
            <span className="animate-pulse">|</span>
          </h1>
          <div className="h-14 flex items-center justify-center">
            {showSubtext && (
              <p className="text-lg text-gray-600 dark:text-gray-300 animate-fade-in">
                This site is under construction. Check back soon!
              </p>
            )}
          </div>
        </div>

        {/* Authentication component for testing */}
        <div className="w-full max-w-md min-h-[200px] flex items-start justify-center">
          {showSubtext && (
            <div className="w-full animate-fade-in">
              <AuthComponent />
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
