import NextAuth, { NextAuthOptions } from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import GitHubProvider from "next-auth/providers/github"
import DiscordProvider from "next-auth/providers/discord"
import { SignJWT } from "jose"

const NEXTAUTH_SESSION_MAX_AGE = 60 * 60 * 24 * 30 // 30 days
const BACKEND_TOKEN_MAX_AGE = 60 * 60 * 2 // 2 hours
const BACKEND_TOKEN_REFRESH_BUFFER = 5 * 60 // 5 minutes

async function mintBackendToken(claims: { sub?: string; email?: string; name?: string }) {
  const now = Math.floor(Date.now() / 1000);
  const exp = now + BACKEND_TOKEN_MAX_AGE;

  const token = await new SignJWT({
    sub: claims.sub,
    email: claims.email,
    name: claims.name,
  })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt(now)
    .setExpirationTime(exp)
    .sign(new TextEncoder().encode(process.env.NEXTAUTH_SECRET!));

  return { token, exp };
}

const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    GitHubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    DiscordProvider({
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    })
  ],
  session: {
    strategy: "jwt",
    maxAge: NEXTAUTH_SESSION_MAX_AGE,
  },
  callbacks: {
    async jwt({ token, user, account, trigger }) {
      // Initial sign in
      if (user) {
        token.sub = user.id
        token.email = user.email
        token.name = user.name
        
        const { token: t, exp } = await mintBackendToken(token);
        token.backendToken = t
        token.backendTokenExpiry = exp
      }
      // Pre-existing access
      // Check if backend token needs refresh (with buffer)
      const shouldRefresh = !token.backendTokenExpiry ||
        Date.now() > (token.backendTokenExpiry as number) - (BACKEND_TOKEN_REFRESH_BUFFER * 1000)

      if (shouldRefresh && token.sub) {
        // Refresh the backend token
        const { token: t, exp } = await mintBackendToken(token);
        token.backendToken = t
        token.backendTokenExpiry = exp
      }
      
      return token
    },
    
    async session({ session, token }) {
      if (token) {
        session.user = {
          id: token.sub as string,
          email: token.email as string,
          name: token.name as string,
        }
        session.accessToken = token.backendToken as string
      }
      return session
    },
  },
  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },
}

const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }