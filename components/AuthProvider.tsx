'use client'

import { SessionProvider } from 'next-auth/react'
import { ReactNode } from 'react'
import { Session } from 'next-auth'

interface AuthProviderProps {
  children: ReactNode
  session?: Session | null
}

export default function AuthProvider({ children, session }: AuthProviderProps) {
  return (
    <SessionProvider basePath="/proxy/auth" session={session}>
      {children}
    </SessionProvider>
  )
}