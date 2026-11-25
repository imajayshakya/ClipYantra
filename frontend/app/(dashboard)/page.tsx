'use client';

import { ReactNode } from 'react';
import Link from 'next/link';
import { Plus, Video, Film, Clock, TrendingUp, Users, ExternalLink } from '@/components/ui/icons';

const stats = [
  { name: 'Total Projects', value: '24', change: '+12%', icon: FolderKanban },
  { name: 'Clips Generated', value: '156', change: '+23%', icon: Film },
  { name: 'Hours Saved', value: '48h', change: '+31%', icon: Clock },
  { name: 'Total Views', value: '1.2M', change: '+45%', icon: TrendingUp },
];

const recentProjects = [
  { id: '1', name: 'Podcast Episode #42', status: 'completed', clips: 8, duration: '45:32', updated: '2 hours ago' },
  { id: '2', name: 'Webinar: AI in 2024', status: 'processing', clips: 0, duration: '1:23:15', updated: '5 hours ago' },
  { id: '3', name: 'Product Launch Video', status: 'draft', clips: 3, duration: '12:45', updated: '1 day ago' },
  { id: '4', name: 'Tutorial Series', status: 'completed', clips: 15, duration: '2:15:30', updated: '3 days ago' },
];

const quickActions = [
  { name: 'New Project', description: 'Upload a video to start', icon: Plus, href: '/dashboard/editor/new', primary: true },
  { name: 'Browse Library', description: 'View all your projects', icon: FolderKanban, href: '/dashboard/library' },
  { name: 'Team Settings', description: 'Manage team members', icon: Users, href: '/dashboard/settings/team' },
  { name: 'API Docs', description: 'Integration guides', icon: ExternalLink, href: '/docs/api', external: true },
];

function FolderKanban({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>
  );
}

function Film({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="2" width="20" height="20" rx="2.18" />
      <line x1="7" y1="2" x2="7" y2="22" />
      <line x1="17" y1="2" x2="17" y2="22" />
      <line x1="2" y1="12" x2="22" y2="12" />
      <line x1="2" y1="7" x2="7" y2="7" />
      <line x1="2" y1="17" x2="7" y2="17" />
      <line x1="17" y1="17" x2="22" y2="17" />
      <line x1="17" y1="7" x2="22" y2="7" />
    </svg>
  );
}

function Clock({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  );
}

function TrendingUp({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
      <polyline points="17 6 23 6 23 12" />
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

function ExternalLink({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
      <polyline points="15 3 21 3 21 9" />
      <line x1="10" y1="14" x2="21" y2="3" />
    </svg>
  );
}

function Plus({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  );
}

function Video({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polygon points="23 7 16 12 23 17 23 7" />
      <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
    </svg>
  );
}

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-display-sm font-bold text-text-primary">Dashboard</h1>
          <p className="mt-1 text-body-md text-text-secondary">
            Overview of your projects and clip generation activity
          </p>
        </div>
        <Link href="/dashboard/editor/new" className="btn-primary">
          <Plus className="h-4 w-4" aria-hidden="true" />
          <span>New Project</span>
        </Link>
      </div>

      {/* Stats grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <article
            key={stat.name}
            className="card p-6 animate-fade-in"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-body-sm font-medium text-text-secondary">{stat.name}</p>
                <p className="mt-2 text-display-md font-bold text-text-primary">{stat.value}</p>
                <p className="mt-1 flex items-center gap-1 text-body-sm font-medium text-success">
                  <span className="h-1.5 w-1.5 rounded-full bg-success" aria-hidden="true" />
                  {stat.change} vs last month
                </p>
              </div>
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-100 text-brand-600 dark:bg-brand-900 dark:text-brand-400">
                <stat.icon className="h-6 w-6" aria-hidden="true" />
              </div>
            </div>
          </article>
        ))}
      </div>

      {/* Quick actions */}
      <section aria-labelledby="quick-actions-heading">
        <h2 id="quick-actions-heading" className="sr-only">Quick actions</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              href={action.href}
              target={action.external ? '_blank' : undefined}
              rel={action.external ? 'noopener noreferrer' : undefined}
              className="card p-6 hover:shadow-lg transition-shadow duration-fast group"
            >
              <div className={clsx(
                'mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl transition-transform duration-fast group-hover:scale-110',
                action.primary ? 'bg-brand-100 text-brand-600 dark:bg-brand-900 dark:text-brand-400' : 'bg-surface-100 text-text-secondary dark:bg-surface-800'
              )}>
                <action.icon className="h-6 w-6" aria-hidden="true" />
              </div>
              <h3 className="mb-1 text-heading-sm font-semibold text-text-primary">{action.name}</h3>
              <p className="text-body-sm text-text-secondary">{action.description}</p>
              {action.external && (
                <ExternalLink className="mt-2 inline-flex h-4 w-4 text-text-muted group-hover:text-text-primary transition-colors" aria-hidden="true" />
              )}
            </Link>
          ))}
        </div>
      </section>

      {/* Recent projects */}
      <section aria-labelledby="recent-projects-heading">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
          <h2 id="recent-projects-heading" className="text-heading-lg font-semibold text-text-primary">
            Recent Projects
          </h2>
          <Link href="/dashboard/library" className="btn-ghost btn-sm">
            View all
          </Link>
        </div>

        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full" role="table">
              <thead>
                <tr className="border-b border-border-default bg-surface-50/50">
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Project</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Status</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Clips</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Duration</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Updated</th>
                  <th className="text-right px-6 py-4 text-body-sm font-medium text-text-secondary">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-default">
                {recentProjects.map((project) => (
                  <tr key={project.id} className="hover:bg-surface-50/50 transition-colors">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-body-md font-medium text-text-primary">{project.name}</p>
                        <p className="text-body-sm text-text-muted">Project ID: {project.id}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={clsx(
                        'badge',
                        project.status === 'completed' && 'badge-success',
                        project.status === 'processing' && 'badge-warning',
                        project.status === 'draft' && 'badge-neutral'
                      )}>
                        {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-body-md text-text-primary">{project.clips}</td>
                    <td className="px-6 py-4 text-body-md text-text-secondary">{project.duration}</td>
                    <td className="px-6 py-4 text-body-sm text-text-muted">{project.updated}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          href={`/dashboard/editor/${project.id}`}
                          className="btn-ghost btn-sm btn-icon"
                          aria-label={`Edit ${project.name}`}
                        >
                          <Video className="h-4 w-4" aria-hidden="true" />
                        </Link>
                        <Link
                          href={`/dashboard/library/${project.id}`}
                          className="btn-ghost btn-sm btn-icon"
                          aria-label={`View details for ${project.name}`}
                        >
                          <ExternalLink className="h-4 w-4" aria-hidden="true" />
                        </Link>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}

import { clsx } from 'clsx';