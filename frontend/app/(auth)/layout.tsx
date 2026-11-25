import { ReactNode } from 'react';

export default function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="min-h-screen flex">
      {/* Brand sidebar on desktop */}
      <aside className="hidden lg:flex lg:w-1/2 flex-col items-center justify-center p-12 bg-brand-600">
        <div className="max-w-md mx-auto text-center">
          <h1 className="mb-4 text-display-lg font-bold text-white">
            ClipYantra
          </h1>
          <p className="text-body-lg text-brand-100">
            Transform long videos into viral short clips with AI-powered editing tools.
          </p>
          <div className="mt-12 space-y-6 text-left">
            {features.map((feature) => (
              <div key={feature.title} className="flex items-start gap-4">
                <div className="flex-shrink-0 mt-0.5 h-6 w-6 text-brand-200">
                  <feature.icon className="h-6 w-6" aria-hidden="true" />
                </div>
                <div>
                  <h3 className="font-medium text-white">{feature.title}</h3>
                  <p className="text-sm text-brand-200">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </aside>

      {/* Auth form area */}
      <main className="flex-1 flex items-center justify-center p-6 lg:p-12">
        <div className="w-full max-w-md">
          <div className="lg:hidden mb-8 text-center">
            <h1 className="text-display-md font-bold text-text-primary">ClipYantra</h1>
            <p className="mt-2 text-body-md text-text-secondary">
              Transform long videos into viral short clips
            </p>
          </div>
          {children}
        </div>
      </main>
    </div>
  );
}

const features = [
  {
    title: 'AI Clip Detection',
    description: 'Automatically find the most engaging moments',
    icon: Sparkles,
  },
  {
    title: 'Smart Transcripts',
    description: 'Accurate transcripts with speaker detection',
    icon: FileText,
  },
  {
    title: 'Multi-Platform Export',
    description: 'Optimized for TikTok, Reels, Shorts',
    icon: Share2,
  },
  {
    title: 'Brand Templates',
    description: 'Consistent branding with customizable templates',
    icon: LayoutTemplate,
  },
];

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