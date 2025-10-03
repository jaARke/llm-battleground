import Link from 'next/link'
import { AlertCircle } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

type ErrorKey =
  | 'Configuration'
  | 'AccessDenied'
  | 'Verification'
  | 'Default'
  | 'OAuthSignin'
  | 'OAuthCallback'
  | 'OAuthCreateAccount'
  | 'EmailCreateAccount'
  | 'Callback'
  | 'OAuthAccountNotLinked'
  | 'EmailSignin'
  | 'CredentialsSignin'
  | 'CredentialsCallback'
  | 'SessionRequired'

const ERROR_MESSAGES: Record<ErrorKey, string> = {
  Configuration:
    'There is a misconfiguration with the authentication service. Please contact support.',
  AccessDenied:
    'You do not have access to sign in with this account. Try a different provider.',
  Verification: 'Your sign-in link may have expired or already been used.',
  Default: 'An unexpected error occurred during sign-in. Please try again.',
  OAuthSignin: 'We could not initiate the provider sign-in. Please try again.',
  OAuthCallback:
    'We could not complete the provider sign-in. Please try again.',
  OAuthCreateAccount: 'We could not create an account with this provider.',
  EmailCreateAccount: 'There was an issue creating an email-based account.',
  Callback:
    'There was an issue handling the sign-in callback. Please try again.',
  OAuthAccountNotLinked:
    'This email is already associated with another account. Sign in using your original provider.',
  EmailSignin: 'We could not send the sign-in email. Please try again later.',
  CredentialsSignin: 'The provided credentials were invalid.',
  CredentialsCallback: 'There was an issue validating your credentials.',
  SessionRequired: 'You need to sign in before accessing this page.',
}

const ERROR_TITLES: Record<ErrorKey, string> = {
  Configuration: 'Configuration issue',
  AccessDenied: 'Access denied',
  Verification: 'Verification required',
  Default: 'Unexpected error',
  OAuthSignin: 'Provider sign-in failed',
  OAuthCallback: 'Provider callback failed',
  OAuthCreateAccount: 'Provider account not created',
  EmailCreateAccount: 'Email account unavailable',
  Callback: 'Callback issue',
  OAuthAccountNotLinked: 'Provider account mismatch',
  EmailSignin: 'Email sign-in failed',
  CredentialsSignin: 'Credentials rejected',
  CredentialsCallback: 'Credentials validation failed',
  SessionRequired: 'Sign-in required',
}

interface ErrorPageProps {
  searchParams: {
    error?: string
  }
}

export default function AuthErrorPage({ searchParams }: ErrorPageProps) {
  const errorKey = (searchParams.error as ErrorKey | undefined) ?? 'Default'
  const errorMessage = ERROR_MESSAGES[errorKey] ?? ERROR_MESSAGES.Default
  const errorTitle = ERROR_TITLES[errorKey] ?? ERROR_TITLES.Default

  return (
    <main className="min-h-screen gradient-bg-primary flex items-center justify-center px-6 py-12">
      <Card variant="glass-panel" className="w-full max-w-xl mx-auto space-y-8">
        <CardHeader className="space-y-3 text-center p-0">
          <Badge
            variant="glass"
            className="mx-auto border-destructive/40 text-destructive"
          >
            Sign in glitch
          </Badge>
          <CardTitle className="text-3xl font-semibold text-foreground">
            Something went wrong
          </CardTitle>
          <CardDescription className="text-base text-muted-foreground">
            We hit a snag connecting to your provider. Check the message below
            and try again.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4 p-0">
          <Alert
            variant="destructive"
            className="border-destructive/40 bg-destructive/10 text-destructive"
          >
            <AlertCircle className="size-4" aria-hidden />
            <AlertTitle className="text-sm font-semibold">
              {errorTitle}
            </AlertTitle>
            <AlertDescription>
              <p>{errorMessage}</p>
            </AlertDescription>
          </Alert>

          <div className="space-y-3 text-sm text-muted-foreground text-center">
            <p>Retry your provider sign-in and make sure popups are allowed.</p>
            <p>
              If the problem continues, email{' '}
              <a
                href="mailto:me@jakerichard.tech"
                className="text-primary font-medium"
              >
                me@jakerichard.tech
              </a>{' '}
              with a screenshot of this page.
            </p>
          </div>
        </CardContent>

        <CardFooter className="p-0">
          <Button variant="glass-primary" className="w-full" asChild>
            <Link href="/auth/signin">
              Try signing in again
            </Link>
          </Button>
        </CardFooter>
      </Card>
    </main>
  )
}
