'use client'

import { ReactNode, useEffect } from 'react'
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import { useSession } from 'next-auth/react'

interface ProtectedRouteProps {
  children: ReactNode
  redirectTo?: string
}

export default function ProtectedRoute({
  children,
  redirectTo,
}: ProtectedRouteProps) {
  const { status } = useSession()
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  useEffect(() => {
    if (status === 'unauthenticated') {
      const params = searchParams.toString()
      const callbackUrl = params ? `${pathname}?${params}` : pathname
      const url = redirectTo
        ? redirectTo
        : `/auth/signin?callbackUrl=${encodeURIComponent(callbackUrl)}`
      router.replace(url)
    }
  }, [status, router, pathname, searchParams, redirectTo])

  if (status === 'loading') {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="text-gray-600 dark:text-gray-300">
          Checking your session…
        </div>
      </div>
    )
  }

  if (status !== 'authenticated') {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="text-gray-600 dark:text-gray-300">
          Redirecting to sign-in…
        </div>
      </div>
    )
  }

  return <>{children}</>
}
