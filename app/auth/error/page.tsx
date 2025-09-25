import Link from 'next/link'

const CARD_CLASSNAMES =
  'w-full max-w-lg mx-auto bg-white/85 dark:bg-gray-900/90 backdrop-blur rounded-3xl shadow-xl border border-gray-200/80 dark:border-red-900/40 p-10 md:p-12 space-y-8'

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

interface ErrorPageProps {
  searchParams: {
    error?: string
  }
}

export default function AuthErrorPage({ searchParams }: ErrorPageProps) {
  const errorKey = (searchParams.error as ErrorKey | undefined) ?? 'Default'
  const message = ERROR_MESSAGES[errorKey] ?? ERROR_MESSAGES.Default

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 flex items-center justify-center px-6 py-12">
      <div className={CARD_CLASSNAMES}>
        <header className="space-y-3 text-center">
          <p className="text-sm uppercase tracking-[0.35em] text-red-500 dark:text-red-400">
            Sign in glitch
          </p>
          <h1 className="text-3xl font-semibold text-gray-900 dark:text-gray-100">
            Something went wrong
          </h1>
        </header>

        <p className="text-base text-center text-rose-600 dark:text-red-400">
          {message}
        </p>

        <div className="space-y-4 text-sm text-center text-gray-600 dark:text-gray-400">
          <p>Retry your provider sign-in and make sure popups are allowed.</p>
          <p>
            If the problem continues, email{' '}
            <a
              href="mailto:me@jakerichard.tech"
              className="text-blue-600 dark:text-blue-400 font-medium"
            >
              me@jakerichard.tech
            </a>{' '}
            with a screenshot of this page.
          </p>
        </div>

        <Link
          href="/auth/signin"
          className="inline-flex justify-center items-center w-full py-3 px-4 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-semibold transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
        >
          Try signing in again
        </Link>
      </div>
    </main>
  )
}
