'use client'

import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

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
    <main className="min-h-screen gradient-bg-primary flex items-center justify-center px-6 py-12">
      <Card variant="glass-panel" className="w-full max-w-3xl mx-auto">
        <CardHeader className="space-y-4 text-center p-0">
          <p className="text-sm uppercase tracking-[0.35em] text-primary">
            LLM Battleground
          </p>
          <CardTitle className="text-4xl font-semibold text-foreground">
            Choose your arena
          </CardTitle>
          <CardDescription className="text-base md:text-lg text-muted-foreground max-w-2xl mx-auto">
            Select a game to launch your next engagement. We will expand the
            roster as new battlegrounds come online.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4 p-0">
          {GAMES.map((game) => (
            <Card key={game.id} variant="glass-card" className="group relative">
              <CardHeader className="flex flex-wrap items-center gap-3 pb-4">
                <Badge variant="glass">
                  {game.status}
                </Badge>
                <span className="text-xs tracking-widest uppercase text-muted-foreground">
                  {game.tagline}
                </span>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <CardTitle className="text-2xl font-semibold text-foreground">
                    {game.name}
                  </CardTitle>
                  <CardDescription className="text-sm md:text-base text-muted-foreground">
                    {game.description}
                  </CardDescription>
                </div>
                <div>
                  <Button asChild variant="glass-primary">
                    <Link href={game.href}>
                      Enter match
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </CardContent>
      </Card>
    </main>
  )
}
