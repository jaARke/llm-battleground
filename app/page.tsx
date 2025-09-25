'use client'

import Link from 'next/link'
import ProtectedRoute from '@/components/ProtectedRoute'

const CARD_CLASSNAMES =
  'w-full max-w-3xl mx-auto bg-white/85 dark:bg-gray-900/85 backdrop-blur rounded-3xl shadow-xl border border-gray-200/70 dark:border-gray-800/70 p-10 md:p-14 space-y-10'

const GAME_CARD_CLASSNAMES =
  'group relative flex flex-col gap-6 rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-900/70 p-6 shadow-sm transition hover:shadow-md'

const CTA_BUTTON_CLASSNAMES =
  'inline-flex items-center justify-center rounded-2xl px-6 py-3 text-sm font-semibold tracking-wide text-white transition focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-600 hover:to-purple-500'

const GAMES = [
  {
    id: 'go-fish',
    name: 'Go Fish',
    tagline: 'LLM-assisted split or steal',
    description:
      'Agents are given the choice between collaboration or competition in an environment with constrained resources.',
    href: '/game/gofish',
    status: 'Available',
  },
]

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 flex items-center justify-center px-6 py-12">
      <div className={CARD_CLASSNAMES}>
        <header className="space-y-4 text-center">
          <p className="text-sm uppercase tracking-[0.35em] text-blue-500 dark:text-blue-400">
            LLM Battleground
          </p>
          <h1 className="text-4xl font-semibold text-gray-900 dark:text-gray-100">
            Choose your arena
          </h1>
          <p className="text-base md:text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Select a game to launch your next engagement. We will expand the
            roster as new battlegrounds come online.
          </p>
        </header>

        <section className="space-y-4">
          {GAMES.map((game) => (
            <article key={game.id} className={GAME_CARD_CLASSNAMES}>
              <div className="flex flex-wrap items-center gap-3">
                <span className="inline-flex items-center rounded-full border border-blue-200/60 dark:border-blue-900/60 bg-blue-50/70 dark:bg-blue-950/40 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-blue-600 dark:text-blue-300">
                  {game.status}
                </span>
                <span className="text-xs tracking-widest uppercase text-gray-400 dark:text-gray-500">
                  {game.tagline}
                </span>
              </div>
              <div className="space-y-2">
                <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
                  {game.name}
                </h2>
                <p className="text-sm md:text-base text-gray-600 dark:text-gray-400">
                  {game.description}
                </p>
              </div>
              <div>
                <Link href={game.href} className={CTA_BUTTON_CLASSNAMES}>
                  Enter match
                </Link>
              </div>
            </article>
          ))}
        </section>
      </div>
    </main>
  )
}
