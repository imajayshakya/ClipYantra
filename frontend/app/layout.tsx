import type { Metadata, Viewport } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
  preload: true,
  fallback: ['system-ui', 'sans-serif'],
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
  preload: true,
  fallback: ['monospace'],
});

export const metadata: Metadata = {
  title: {
    default: 'ClipYantra - AI-Powered Video Editing',
    template: '%s | ClipYantra',
  },
  description: 'Transform long-form content into engaging short clips with AI-powered editing tools.',
  keywords: ['video editing', 'AI', 'short clips', 'content creation', 'social media'],
  authors: [{ name: 'ClipYantra Team' }],
  creator: 'ClipYantra',
  publisher: 'ClipYantra',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://clipyantra.com',
    siteName: 'ClipYantra',
    title: 'ClipYantra - AI-Powered Video Editing',
    description: 'Transform long-form content into engaging short clips with AI-powered editing tools.',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'ClipYantra',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ClipYantra - AI-Powered Video Editing',
    description: 'Transform long-form content into engaging short clips with AI-powered editing tools.',
    images: ['/og-image.png'],
    creator: '@clipyantra',
  },
  verification: {
    google: 'google-site-verification-code',
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#09090b' },
  ],
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://api.clipyantra.com" />
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="icon" href="/icon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className="min-h-screen bg-background-primary text-text-primary antialiased">
        {children}
      </body>
    </html>
  );
}