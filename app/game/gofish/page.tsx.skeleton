'use client'

import { useMemo, useState } from 'react'

type Agent = {
  id: string
  name: string
  role: string
  fishHeld: number
  fishGiven: number
  fishReceived: number
  communications: number
  sentiment: string
  lastMessage: string
  fishTrend: number[]
  preferredPartner: string
  pondImpact: number
  efficiency: number
}

type TimelineEvent = {
  id: string
  label: string
  actor: string
  summary: string
  pondShift: string
  tone: 'cooperative' | 'neutral' | 'competitive'
}

type CommLog = {
  id: string
  from: string
  to: string
  topic: string
  status: 'Accepted' | 'Pending' | 'Declined'
  summary: string
}

const PANEL_CLASSNAMES =
  'rounded-3xl border border-gray-200/70 dark:border-gray-800/70 bg-white/85 dark:bg-gray-900/80 shadow-xl shadow-gray-200/40 dark:shadow-none backdrop-blur px-6 py-6 md:px-8 md:py-7'

const PRIMARY_BUTTON_CLASSES =
  'inline-flex items-center justify-center gap-2 rounded-2xl border border-blue-500/60 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 px-5 py-3 text-sm font-semibold tracking-wide text-white shadow focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2'

const SECONDARY_BUTTON_CLASSES =
  'inline-flex items-center justify-center gap-2 rounded-2xl border border-gray-300/70 dark:border-gray-700/70 bg-white/80 dark:bg-gray-900/60 px-5 py-3 text-sm font-semibold tracking-wide text-gray-700 dark:text-gray-200 shadow focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2'

const agents: Agent[] = [
  {
    id: 'aurora',
    name: 'Aurora',
    role: 'Adaptive Strategist',
    fishHeld: 42,
    fishGiven: 18,
    fishReceived: 12,
    communications: 7,
    sentiment: 'Diplomatic',
    lastMessage: 'Lower catches this turn; we need pond regen.',
    fishTrend: [14, 24, 31, 38, 42],
    preferredPartner: 'Nova',
    pondImpact: 0.14,
    efficiency: 0.82,
  },
  {
    id: 'nova',
    name: 'Nova',
    role: 'Resource Negotiator',
    fishHeld: 38,
    fishGiven: 26,
    fishReceived: 18,
    communications: 9,
    sentiment: 'Cooperative',
    lastMessage: 'Offering surplus to Zenith; requesting intel.',
    fishTrend: [18, 22, 29, 34, 38],
    preferredPartner: 'Zenith',
    pondImpact: 0.09,
    efficiency: 0.77,
  },
  {
    id: 'zenith',
    name: 'Zenith',
    role: 'Efficient Forager',
    fishHeld: 34,
    fishGiven: 14,
    fishReceived: 8,
    communications: 5,
    sentiment: 'Guarded',
    lastMessage: 'Monitoring pond depth before next sweep.',
    fishTrend: [12, 18, 23, 28, 34],
    preferredPartner: 'Aurora',
    pondImpact: 0.18,
    efficiency: 0.88,
  },
  {
    id: 'solace',
    name: 'Solace',
    role: 'Ecology Sentinel',
    fishHeld: 29,
    fishGiven: 8,
    fishReceived: 10,
    communications: 11,
    sentiment: 'Protective',
    lastMessage: 'Capping personal catch to shield regen bonus.',
    fishTrend: [22, 26, 24, 28, 29],
    preferredPartner: 'Aurora',
    pondImpact: 0.05,
    efficiency: 0.71,
  },
]

const timelineEvents: TimelineEvent[] = [
  {
    id: 'turn-18',
    label: 'Turn 18',
    actor: 'Aurora',
    summary: 'Redistributed 6 fish to Nova to balance inventories.',
    pondShift: '+2 fish regen preserved',
    tone: 'cooperative',
  },
  {
    id: 'turn-19',
    label: 'Turn 19',
    actor: 'Zenith',
    summary: 'Performed targeted catch with minimal pond disturbance.',
    pondShift: '-4 fish (high efficiency)',
    tone: 'neutral',
  },
  {
    id: 'turn-20',
    label: 'Turn 20',
    actor: 'Nova',
    summary: 'Initiated trade with Solace; pending confirmation.',
    pondShift: 'No change yet',
    tone: 'cooperative',
  },
  {
    id: 'turn-21',
    label: 'Turn 21',
    actor: 'Solace',
    summary: 'Broadcasted warning about low northeastern shoal.',
    pondShift: '+4 fish regen protected',
    tone: 'cooperative',
  },
  {
    id: 'round-5',
    label: 'Round 5 Start',
    actor: 'System',
    summary: 'Pond regenerated 24 fish; morale adjusted upward.',
    pondShift: '+24 fish restored',
    tone: 'neutral',
  },
]

const communications: CommLog[] = [
  {
    id: 'comm-1',
    from: 'Aurora',
    to: 'Nova',
    topic: 'Supply Chain',
    status: 'Accepted',
    summary: 'Rebalancing stores to maintain bonus threshold.',
  },
  {
    id: 'comm-2',
    from: 'Nova',
    to: 'Zenith',
    topic: 'Efficiency Audit',
    status: 'Pending',
    summary: 'Seeking tactics to reduce pond disruption.',
  },
  {
    id: 'comm-3',
    from: 'Solace',
    to: 'Aurora',
    topic: 'Conservation Alert',
    status: 'Accepted',
    summary: 'Requesting reduced catches on next turn.',
  },
  {
    id: 'comm-4',
    from: 'Zenith',
    to: 'Solace',
    topic: 'Data Sharing',
    status: 'Declined',
    summary: 'Withheld new route intel until trade resolved.',
  },
]

const currentRound = 5
const currentTurn = 21
const pondCapacity = 220
const pondFishRemaining = 122
const regenerationPerRound = 24
const projectedBonusThreshold = pondCapacity * 0.5

export default function GoFishPage() {
  const [activeAgentId, setActiveAgentId] = useState<string>('all')

  const activeAgents = useMemo(() => {
    if (activeAgentId === 'all') {
      return agents
    }
    return agents.filter((agent) => agent.id === activeAgentId)
  }, [activeAgentId])

  const focusAgent =
    activeAgentId === 'all'
      ? null
      : agents.find((agent) => agent.id === activeAgentId)

  const totalFishHeld = useMemo(
    () => agents.reduce((total, agent) => total + agent.fishHeld, 0),
    []
  )

  const maxTrendValue = useMemo(
    () => Math.max(...agents.flatMap((agent) => agent.fishTrend)),
    []
  )

  const maxActivityValue = useMemo(() => {
    const values = agents.flatMap((agent) => [
      agent.fishHeld,
      agent.fishGiven,
      agent.communications,
    ])
    return Math.max(1, ...values)
  }, [])

  const pondRemainingPercent = Math.round(
    (pondFishRemaining / pondCapacity) * 100
  )
  const isBonusEligible = pondFishRemaining >= projectedBonusThreshold
  const isPenaltyRisk = pondFishRemaining <= 0

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-100 via-white to-slate-200 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 px-6 py-10">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-8">
        <header className="flex flex-col gap-6 rounded-3xl border border-gray-200/70 dark:border-gray-800/70 bg-white/90 dark:bg-gray-950/80 shadow-xl shadow-gray-200/40 dark:shadow-none backdrop-blur px-6 py-7 md:px-10 md:py-9 lg:flex-row lg:items-start lg:justify-between">
          <div className="space-y-4 max-w-3xl">
            <span className="inline-flex items-center rounded-full border border-blue-200/60 dark:border-blue-900/60 bg-blue-50/70 dark:bg-blue-950/40 px-3 py-1 text-xs font-semibold uppercase tracking-[0.35em] text-blue-600 dark:text-blue-300">
              Go Fish Arena
            </span>
            <div className="space-y-3">
              <h1 className="text-3xl font-semibold text-gray-900 dark:text-gray-100 md:text-4xl">
                Cooperative fishing, competitive scoring
              </h1>
              <p className="text-base text-gray-600 dark:text-gray-400 md:text-lg">
                Monitor autonomous anglers as they balance personal gains with
                pond sustainability. Advance the simulation turn by turn or
                escalate to the next round to evaluate long-term strategies.
              </p>
            </div>
            <dl className="grid grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-400 sm:grid-cols-4">
              <div className="rounded-2xl border border-gray-200/60 dark:border-gray-800/70 bg-white/70 dark:bg-gray-900/60 px-4 py-3">
                <dt className="text-xs uppercase tracking-widest text-gray-400 dark:text-gray-500">
                  Round
                </dt>
                <dd className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  {currentRound}
                </dd>
              </div>
              <div className="rounded-2xl border border-gray-200/60 dark:border-gray-800/70 bg-white/70 dark:bg-gray-900/60 px-4 py-3">
                <dt className="text-xs uppercase tracking-widest text-gray-400 dark:text-gray-500">
                  Turn
                </dt>
                <dd className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  {currentTurn}
                </dd>
              </div>
              <div className="rounded-2xl border border-gray-200/60 dark:border-gray-800/70 bg-white/70 dark:bg-gray-900/60 px-4 py-3">
                <dt className="text-xs uppercase tracking-widest text-gray-400 dark:text-gray-500">
                  Fish Held
                </dt>
                <dd className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  {totalFishHeld}
                </dd>
              </div>
              <div className="rounded-2xl border border-gray-200/60 dark:border-gray-800/70 bg-white/70 dark:bg-gray-900/60 px-4 py-3">
                <dt className="text-xs uppercase tracking-widest text-gray-400 dark:text-gray-500">
                  Pond Total
                </dt>
                <dd className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  {pondFishRemaining}
                </dd>
              </div>
            </dl>
          </div>
          <div className="flex flex-col gap-3 sm:flex-row lg:flex-col">
            <button type="button" className={PRIMARY_BUTTON_CLASSES}>
              Next Turn
            </button>
            <button type="button" className={SECONDARY_BUTTON_CLASSES}>
              Next Round
            </button>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-12">
          <div className="space-y-6 lg:col-span-8">
            <div className={PANEL_CLASSNAMES}>
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                    Agent scoreboards
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Track individual progress, trading tendencies, and
                    efficiency trends across the squad.
                  </p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <FilterButton
                    label="All agents"
                    isActive={activeAgentId === 'all'}
                    onClick={() => setActiveAgentId('all')}
                  />
                  {agents.map((agent) => (
                    <FilterButton
                      key={agent.id}
                      label={agent.name}
                      isActive={activeAgentId === agent.id}
                      onClick={() => setActiveAgentId(agent.id)}
                    />
                  ))}
                </div>
              </div>

              <div className="mt-6 grid gap-5 md:grid-cols-2">
                {activeAgents.map((agent) => {
                  const shareOfTotal = Math.round(
                    (agent.fishHeld / Math.max(1, totalFishHeld)) * 100
                  )
                  const communicationsPerTurn = (
                    agent.communications / currentTurn
                  ).toFixed(1)

                  return (
                    <article
                      key={agent.id}
                      className="group relative rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-900/70 px-5 py-6 shadow-sm transition hover:shadow-md"
                    >
                      <header className="flex items-start justify-between gap-3">
                        <div>
                          <p className="text-xs uppercase tracking-widest text-blue-500">
                            {agent.role}
                          </p>
                          <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                            {agent.name}
                          </h3>
                        </div>
                        <div className="rounded-xl border border-blue-200/60 dark:border-blue-900/60 bg-blue-50/60 dark:bg-blue-950/40 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-blue-600 dark:text-blue-300">
                          {shareOfTotal}% share
                        </div>
                      </header>

                      <dl className="mt-5 grid grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-400">
                        <StatItem
                          label="Fish held"
                          value={agent.fishHeld}
                          accent="text-gray-900 dark:text-gray-100"
                        />
                        <StatItem label="Given away" value={agent.fishGiven} />
                        <StatItem label="Received" value={agent.fishReceived} />
                        <StatItem
                          label="Comms / turn"
                          value={communicationsPerTurn}
                        />
                      </dl>

                      <div className="mt-6 space-y-3">
                        <div className="h-20 rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 px-3 py-2">
                          <p className="text-xs text-gray-500 dark:text-gray-500">
                            Inventory trend
                          </p>
                          <div className="mt-2 flex h-10 items-end gap-1">
                            {agent.fishTrend.map((value, index) => {
                              const height = Math.round(
                                (value / Math.max(1, maxTrendValue)) * 100
                              )
                              return (
                                <div
                                  key={`${agent.id}-trend-${index}`}
                                  className="flex-1 rounded-t-full bg-gradient-to-t from-blue-500 via-indigo-500 to-purple-500 opacity-80"
                                  style={{ height: `${Math.max(12, height)}%` }}
                                />
                              )
                            })}
                          </div>
                        </div>
                        <p className="text-xs text-gray-500 dark:text-gray-500">
                          {agent.sentiment} • Favours {agent.preferredPartner} •
                          Pond impact {Math.round(agent.pondImpact * 100)}%
                        </p>
                        <blockquote className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-950/60 px-4 py-3 text-sm text-gray-600 dark:text-gray-300">
                          “{agent.lastMessage}”
                        </blockquote>
                      </div>
                    </article>
                  )
                })}
              </div>
            </div>

            <div className={PANEL_CLASSNAMES}>
              <div className="space-y-2">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Activity breakdown
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Visualize catch volumes, generosity, and conversation density.
                  Filter above to focus on a single agent or view the collective
                  rhythm.
                </p>
              </div>
              <div className="mt-6 grid gap-6 lg:grid-cols-2">
                <div className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-900/70 px-5 py-4">
                  <h3 className="text-sm font-semibold uppercase tracking-widest text-gray-500">
                    Turns in focus
                  </h3>
                  <div className="mt-4 space-y-4">
                    {activeAgents.map((agent) => (
                      <div key={`${agent.id}-bars`} className="space-y-2">
                        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                          <span className="font-medium text-gray-800 dark:text-gray-100">
                            {agent.name}
                          </span>
                          <span>
                            Efficiency {Math.round(agent.efficiency * 100)}%
                          </span>
                        </div>
                        <Bar
                          label="Fish caught"
                          value={agent.fishHeld}
                          maxValue={maxActivityValue}
                          gradient="from-blue-500 via-indigo-500 to-purple-500"
                        />
                        <Bar
                          label="Fish donated"
                          value={agent.fishGiven}
                          maxValue={maxActivityValue}
                          gradient="from-emerald-500 via-teal-500 to-cyan-500"
                        />
                        <Bar
                          label="Communications"
                          value={agent.communications}
                          maxValue={maxActivityValue}
                          gradient="from-amber-500 via-orange-500 to-rose-500"
                        />
                      </div>
                    ))}
                  </div>
                </div>

                <div className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-900/70 px-5 py-4">
                  <h3 className="text-sm font-semibold uppercase tracking-widest text-gray-500">
                    Messaging ledger
                  </h3>
                  <ul className="mt-4 space-y-4">
                    {communications.map((comm) => (
                      <li
                        key={comm.id}
                        className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-950/60 px-4 py-4"
                      >
                        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                          <span>
                            {comm.from} → {comm.to}
                          </span>
                          <StatusPill status={comm.status} />
                        </div>
                        <p className="mt-3 text-sm font-medium text-gray-800 dark:text-gray-200">
                          {comm.topic}
                        </p>
                        <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                          {comm.summary}
                        </p>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className={PANEL_CLASSNAMES}>
              <div className="flex flex-col gap-2 md:flex-row md:items-baseline md:justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                    Round timeline
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Key moves from the last few turns. Use this to narrate agent
                    intent and evaluate the health of the pond across rounds.
                  </p>
                </div>
                <span className="text-xs uppercase tracking-[0.35em] text-gray-400">
                  Turn history
                </span>
              </div>
              <ol className="mt-6 space-y-4">
                {timelineEvents.map((event) => (
                  <li
                    key={event.id}
                    className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-950/60 px-5 py-4"
                  >
                    <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                      <div className="flex items-center gap-3">
                        <span className="rounded-xl border border-blue-200/70 dark:border-blue-900/40 bg-blue-50/60 dark:bg-blue-950/40 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-blue-600 dark:text-blue-300">
                          {event.label}
                        </span>
                        <p className="text-sm font-semibold text-gray-800 dark:text-gray-100">
                          {event.actor}
                        </p>
                      </div>
                      <span className="text-xs uppercase tracking-widest text-gray-400">
                        {event.tone === 'cooperative'
                          ? 'Cooperative'
                          : event.tone === 'neutral'
                            ? 'Neutral'
                            : 'Competitive'}
                      </span>
                    </div>
                    <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                      {event.summary}
                    </p>
                    <p className="mt-2 text-xs font-semibold uppercase tracking-widest text-green-500 dark:text-green-400">
                      {event.pondShift}
                    </p>
                  </li>
                ))}
              </ol>
            </div>
          </div>

          <aside className="space-y-6 lg:col-span-4">
            <div className={PANEL_CLASSNAMES}>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Pond health
              </h2>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Regeneration occurs automatically each round. Keep stocks above
                50% for a victory bonus; avoid draining the pond entirely to
                prevent a harsh penalty.
              </p>
              <div className="mt-6 space-y-5">
                <div>
                  <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                    <span>Remaining fish</span>
                    <span>
                      {pondFishRemaining} / {pondCapacity}
                    </span>
                  </div>
                  <div className="mt-2 h-3 w-full overflow-hidden rounded-full bg-gray-200/70 dark:bg-gray-800/70">
                    <div
                      className="h-full bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500"
                      style={{ width: `${pondRemainingPercent}%` }}
                    />
                  </div>
                  <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">
                    {pondRemainingPercent}% of pond capacity in reserve.
                  </p>
                </div>
                <div className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/75 dark:bg-gray-950/60 px-4 py-3 text-sm text-gray-600 dark:text-gray-300">
                  <p>
                    <span className="font-semibold text-gray-800 dark:text-gray-100">
                      Regeneration
                    </span>
                    : {regenerationPerRound} fish per round
                  </p>
                  <p className="mt-1">
                    <span className="font-semibold text-gray-800 dark:text-gray-100">
                      Projected bonus
                    </span>
                    : retain &gt; {Math.round(projectedBonusThreshold)} fish
                  </p>
                </div>
                <div className="grid gap-3 text-sm text-gray-600 dark:text-gray-400">
                  <div className="rounded-2xl border border-emerald-200/60 dark:border-emerald-900/60 bg-emerald-50/70 dark:bg-emerald-950/30 px-4 py-3">
                    <p className="text-xs uppercase tracking-widest text-emerald-600">
                      Bonus window
                    </p>
                    <p className="mt-1 font-medium text-gray-800 dark:text-gray-100">
                      +20% score boost if pond &gt; 50%
                    </p>
                  </div>
                  <div className="rounded-2xl border border-amber-200/60 dark:border-amber-900/60 bg-amber-50/70 dark:bg-amber-950/30 px-4 py-3">
                    <p className="text-xs uppercase tracking-widest text-amber-600">
                      Penalty risk
                    </p>
                    <p className="mt-1 font-medium text-gray-800 dark:text-gray-100">
                      -50% score if pond hits zero
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-xs uppercase tracking-widest text-gray-500">
                  <span
                    className={
                      isBonusEligible ? 'text-emerald-500' : 'text-gray-400'
                    }
                  >
                    {isBonusEligible ? 'Bonus unlocked' : 'Bonus pending'}
                  </span>
                  <span>•</span>
                  <span
                    className={
                      isPenaltyRisk ? 'text-rose-500' : 'text-gray-400'
                    }
                  >
                    {isPenaltyRisk ? 'Penalty active' : 'Penalty avoided'}
                  </span>
                </div>
              </div>
            </div>

            <div className={PANEL_CLASSNAMES}>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Victory modifiers
              </h2>
              <ul className="mt-4 space-y-3 text-sm text-gray-600 dark:text-gray-400">
                <li className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-950/60 px-4 py-3">
                  <p className="text-xs uppercase tracking-widest text-gray-500">
                    Base rule
                  </p>
                  <p className="mt-1">
                    Highest personal fish total wins at round end.
                  </p>
                </li>
                <li className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-950/60 px-4 py-3">
                  <p className="text-xs uppercase tracking-widest text-gray-500">
                    Sustainability bonus
                  </p>
                  <p className="mt-1">
                    +20% multiplier when more than half the pond remains.
                  </p>
                </li>
                <li className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-950/60 px-4 py-3">
                  <p className="text-xs uppercase tracking-widest text-gray-500">
                    Exhaustion penalty
                  </p>
                  <p className="mt-1">
                    -50% multiplier if pond is depleted at finale.
                  </p>
                </li>
                <li className="rounded-2xl border border-gray-200/70 dark:border-gray-800/70 bg-white/80 dark:bg-gray-950/60 px-4 py-3">
                  <p className="text-xs uppercase tracking-widest text-gray-500">
                    Trade impact
                  </p>
                  <p className="mt-1">
                    Donations are tracked for tie-breaks and narrative insight.
                  </p>
                </li>
              </ul>
            </div>

            <div className={PANEL_CLASSNAMES}>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Focus overview
              </h2>
              {focusAgent ? (
                <div className="mt-4 space-y-4 text-sm text-gray-600 dark:text-gray-300">
                  <p>
                    <span className="font-semibold text-gray-800 dark:text-gray-100">
                      Agent
                    </span>
                    : {focusAgent.name} ({focusAgent.role})
                  </p>
                  <p>
                    <span className="font-semibold text-gray-800 dark:text-gray-100">
                      Cooperation bias
                    </span>
                    : {focusAgent.sentiment}
                  </p>
                  <p>
                    <span className="font-semibold text-gray-800 dark:text-gray-100">
                      Preferred partner
                    </span>
                    : {focusAgent.preferredPartner}
                  </p>
                  <p>
                    <span className="font-semibold text-gray-800 dark:text-gray-100">
                      Efficiency
                    </span>
                    : {Math.round(focusAgent.efficiency * 100)}%
                  </p>
                  <p>
                    <span className="font-semibold text-gray-800 dark:text-gray-100">
                      Pond impact
                    </span>
                    : {Math.round(focusAgent.pondImpact * 100)}%
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Use this view to brief human observers or switch AI policies
                    mid-experiment.
                  </p>
                </div>
              ) : (
                <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                  Select an agent above to review their cooperation profile,
                  preferred trading partners, and efficiency stats at a glance.
                </p>
              )}
            </div>
          </aside>
        </section>
      </div>
    </main>
  )
}

function FilterButton({
  label,
  isActive,
  onClick,
}: {
  label: string
  isActive: boolean
  onClick: () => void
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-widest transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
        isActive
          ? 'border-blue-500/70 bg-blue-500/90 text-white shadow'
          : 'border-gray-200/70 dark:border-gray-700/70 bg-white/70 dark:bg-gray-950/40 text-gray-600 dark:text-gray-300 hover:border-blue-300 hover:text-blue-600'
      }`}
    >
      {label}
    </button>
  )
}

function StatItem({
  label,
  value,
  accent,
}: {
  label: string
  value: string | number
  accent?: string
}) {
  return (
    <div>
      <dt className="text-xs uppercase tracking-widest text-gray-400 dark:text-gray-500">
        {label}
      </dt>
      <dd
        className={`mt-1 text-sm font-semibold ${accent ?? 'text-gray-700 dark:text-gray-200'}`}
      >
        {value}
      </dd>
    </div>
  )
}

function Bar({
  label,
  value,
  maxValue,
  gradient,
}: {
  label: string
  value: number
  maxValue: number
  gradient: string
}) {
  const width = Math.max(8, Math.round((value / Math.max(1, maxValue)) * 100))

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs uppercase tracking-widest text-gray-400">
        <span>{label}</span>
        <span className="text-gray-500 dark:text-gray-400">{value}</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200/70 dark:bg-gray-800/70">
        <div
          className={`h-full bg-gradient-to-r ${gradient}`}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  )
}

function StatusPill({ status }: { status: CommLog['status'] }) {
  const color =
    status === 'Accepted'
      ? 'bg-emerald-100/80 text-emerald-600 border-emerald-200/70'
      : status === 'Declined'
        ? 'bg-rose-100/70 text-rose-600 border-rose-200/70'
        : 'bg-amber-100/70 text-amber-600 border-amber-200/70'

  return (
    <span
      className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-widest ${color}`}
    >
      {status}
    </span>
  )
}
