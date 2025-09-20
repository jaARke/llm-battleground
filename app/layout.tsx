import { Metadata, Viewport } from "next";
import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const viewport: Viewport = {
  themeColor: "#111827",
  colorScheme: "light dark",
  viewportFit: "cover",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export const metadata: Metadata = {
  metadataBase: new URL("https://llmbattles.jakerichard.tech"),
  title: "LLM Battles │ AI Showdown",
  description: "Language models face off in a suite of classic turn-based strategy games.",
  openGraph: {
    type: "website",
    url: "/",
    title: "LLM Battles │ AI Showdown",
    description: "Language models face off in a suite of classic turn-based strategy games.",
    siteName: "Language Model Battleground",
    images: [
      {
        url: "/og/og-image.png",
        width: 1200,
        height: 630,
        alt: "Turn-based strategy battles between language models",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "LLM Battles │ AI Showdown",
    description: "Language models face off in a suite of classic turn-based strategy games.",
    images: ["/og/og-image.png"],
  },
  icons: {
    icon: [
      { url: "/icons/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/icons/favicon-32x32.png", sizes: "32x32", type: "image/png" },
    ],
    apple: "/icons/apple-touch-icon.png",
    shortcut: "/icons/favicon.ico",
    other: [
      {
        rel: "android-chrome",
        url: "/icons/android-chrome-192x192.png",
        sizes: "192x192",
      },
      {
        rel: "android-chrome",
        url: "/icons/android-chrome-512x512.png",
        sizes: "512x512",
      },
    ],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}