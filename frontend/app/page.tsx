import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <section className="relative flex-1 flex items-center justify-center overflow-hidden bg-gradient-to-b from-brand-50 to-white dark:from-surface-950 dark:to-surface-900">
        <div className="container relative z-10 py-20">
          <div className="max-w-3xl mx-auto text-center">
            <div className="mb-8 animate-fade-in">
              <span className="inline-flex items-center gap-2 rounded-full bg-brand-100 px-4 py-1.5 text-body-sm font-medium text-brand-700 dark:bg-brand-900 dark:text-brand-300">
                <span className="relative flex h-1.5 w-1.5">
                  <span className="animate-ping absolute inset-0 h-full w-full rounded-full bg-brand-500 opacity-75"></span>
                  <span className="relative block h-full w-full rounded-full bg-brand-500"></span>
                </span>
                New: AI Clip Generation v2.0
              </span>
            </div>

            <h1 className="mb-6 text-display-xl font-bold text-text-primary animate-slide-up">
              Transform Long Videos into{' '}
              <span className="gradient-text">Viral Short Clips</span>
              {' '}in Minutes
            </h1>

            <p className="mb-10 text-body-lg text-text-secondary max-w-2xl mx-auto animate-slide-up" style={{ animationDelay: '100ms' }}>
              Upload your content, let AI find the best moments, and publish directly to social platforms.
              No editing experience required.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up" style={{ animationDelay: '200ms' }}>
              <Link
                href="/login"
                className="btn-primary btn-lg w-full sm:w-auto"
              >
                Get Started Free
              </Link>
              <Link
                href="/login"
                className="btn-outline btn-lg w-full sm:w-auto"
              >
                Watch Demo
              </Link>
            </div>

            <div className="mt-16 animate-fade-in" style={{ animationDelay: '300ms' }}>
              <p className="text-body-sm text-text-muted mb-4">Trusted by creators worldwide</p>
              <div className="flex items-center justify-center gap-8 opacity-40">
                <span className="text-body-xs font-medium text-text-muted">YouTube</span>
                <span className="text-body-xs font-medium text-text-muted">TikTok</span>
                <span className="text-body-xs font-medium text-text-muted">Instagram</span>
                <span className="text-body-xs font-medium text-text-muted">LinkedIn</span>
              </div>
            </div>
          </div>
        </div>

        {/* Background decoration */}
        <div className="absolute inset-0 -z-10 overflow-hidden" aria-hidden="true">
          <div className="absolute top-20 left-10 h-72 w-72 rounded-full bg-brand-200/30 blur-3xl animate-pulse" />
          <div className="absolute bottom-20 right-10 h-72 w-72 rounded-full bg-brand-300/20 blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-brand-100/20 blur-3xl" />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-background-primary dark:bg-surface-950">
        <div className="container">
          <div className="max-w-2xl mx-auto text-center mb-16">
            <h2 className="mb-4 text-display-md font-bold text-text-primary">
              Everything you need to create engaging clips
            </h2>
            <p className="text-body-lg text-text-secondary">
              Powerful AI tools designed for modern content creators
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <article
                key={feature.title}
                className="card group p-6 animate-fade-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-100 text-brand-600 dark:bg-brand-900 dark:text-brand-400 group-hover:scale-110 transition-transform duration-fast">
                  <feature.icon className="h-6 w-6" aria-hidden="true" />
                </div>
                <h3 className="mb-2 text-heading-md font-semibold text-text-primary">
                  {feature.title}
                </h3>
                <p className="text-body-md text-text-secondary">
                  {feature.description}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-surface-900 dark:bg-surface-950">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="mb-4 text-display-sm font-bold text-white">
              Ready to start creating?
            </h2>
            <p className="mb-8 text-body-lg text-surface-300">
              Join thousands of creators saving hours every week with ClipYantra.
            </p>
            <Link
              href="/login"
              className="btn-primary btn-lg inline-flex"
            >
              Start Free Trial
            </Link>
            <p className="mt-4 text-body-sm text-surface-500">
              No credit card required · 14-day free trial · Cancel anytime
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-background-primary border-t border-border-default dark:bg-surface-950 dark:border-surface-800">
        <div className="container">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2">
              <span className="text-heading-sm font-bold text-text-primary">ClipYantra</span>
            </div>
            <nav className="flex flex-wrap items-center justify-center gap-6 text-body-sm text-text-secondary">
              <Link href="/about" className="hover:text-text-primary transition-colors">About</Link>
              <Link href="/pricing" className="hover:text-text-primary transition-colors">Pricing</Link>
              <Link href="/docs" className="hover:text-text-primary transition-colors">Docs</Link>
              <Link href="/blog" className="hover:text-text-primary transition-colors">Blog</Link>
              <Link href="/privacy" className="hover:text-text-primary transition-colors">Privacy</Link>
              <Link href="/terms" className="hover:text-text-primary transition-colors">Terms</Link>
            </nav>
            <p className="text-body-xs text-text-muted">
              © {new Date().getFullYear()} ClipYantra. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}

const features = [
  {
    title: 'AI Clip Detection',
    description: 'Automatically identify the most engaging moments from your long-form content using advanced ML models.',
    icon: Sparkles,
  },
  {
    title: 'Smart Transcripts',
    description: 'Generate accurate transcripts with speaker detection, timestamps, and searchable content.',
    icon: FileText,
  },
  {
    title: 'Multi-Platform Export',
    description: 'One-click export optimized for TikTok, Reels, Shorts, and LinkedIn with platform-specific aspect ratios.',
    icon: Share2,
  },
  {
    title: 'Brand Templates',
    description: 'Consistent branding with customizable templates, lower thirds, captions, and color schemes.',
    icon: LayoutTemplate,
  },
  {
    title: 'Team Collaboration',
    description: 'Real-time collaboration with comments, approvals, and version control for seamless teamwork.',
    icon: Users,
  },
  {
    title: 'Analytics Dashboard',
    description: 'Track performance across platforms with unified analytics and AI-powered optimization suggestions.',
    icon: BarChart3,
  },
];

// Icon components (inline for simplicity)
function Sparkles({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2v20M17 5H7M17 19H7M2 12h20M5 5l7 7M19 5l-7 7M5 19l7-7M19 19l-7-7" />
    </svg>
  );
}

function FileText({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
      <polyline points="10 9 9 9 8 9" />
    </svg>
  );
}

function Share2({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="18" cy="5" r="3" />
      <circle cx="6" cy="12" r="3" />
      <circle cx="18" cy="19" r="3" />
      <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
      <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
    </svg>
  );
}

function LayoutTemplate({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <line x1="3" y1="9" x2="21" y2="9" />
      <line x1="9" y1="21" x2="9" y2="9" />
    </svg>
  );
}

function Users({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function BarChart3({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  );
}