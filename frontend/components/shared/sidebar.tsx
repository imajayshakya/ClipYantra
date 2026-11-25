'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { IconButton } from '@/components/ui';
import { useProjectStore } from '@/store';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: 'layout-dashboard' },
  { name: 'Library', href: '/dashboard/library', icon: 'library' },
  { name: 'Editor', href: '/dashboard/editor', icon: 'clapperboard' },
  { name: 'Settings', href: '/dashboard/settings', icon: 'settings' },
];

const icons: Record<string, React.ReactNode> = {
  'layout-dashboard': (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
  ),
  library: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
  ),
  clapperboard: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 18a3 3 0 000-6H6a3 3 0 000 6h3z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 18a3 3 0 010-6h3a3 3 0 010 6h-3z" /></svg>
  ),
  settings: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
  ),
  chevronLeft: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
  ),
  chevronRight: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
  ),
  plus: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
  ),
  folder: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
  ),
  recent: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
  ),
  star: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>
  ),
  archive: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" /></svg>
  ),
  trash: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
  ),
};

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  collapsed?: boolean;
  onToggleCollapse?: () => void;
}

export function Sidebar({ open, onClose, collapsed = false, onToggleCollapse }: SidebarProps) {
  const pathname = usePathname();
  const { projects, currentProject, sidebarOpen: storeSidebarOpen } = useProjectStore();

  // Sync with store
  React.useEffect(() => {
    if (open !== storeSidebarOpen) {
      // Don't trigger store update from here to avoid loops
    }
  }, [open, storeSidebarOpen]);

  const recentProjects = projects.slice(0, 5);
  const starredProjects = projects.filter(p => p.tags.includes('starred')).slice(0, 5);

  if (!open && !collapsed) return null;

  return (
    <>
      {/* Backdrop for mobile */}
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed lg:relative inset-y-0 left-0 z-50 flex flex-col transition-all duration-300 ease-in-out border-r border-surface-200 bg-surface-50 dark:border-surface-700 dark:bg-surface-900',
          collapsed ? 'w-20' : 'w-64',
          open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
        aria-label="Sidebar navigation"
      >
        {/* Logo & collapse toggle */}
        <div className="flex h-16 items-center justify-between px-4 border-b border-surface-200 dark:border-surface-700">
          {!collapsed && (
            <Link href="/dashboard" className="flex items-center gap-2" aria-label="ClipYantra Dashboard">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600">
                <svg className="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span className="font-bold text-xl text-surface-900 dark:text-white">ClipYantra</span>
            </Link>
          )}

          <IconButton
            onClick={onToggleCollapse}
            className={cn('flex-shrink-0', collapsed && 'ml-auto')}
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            variant="ghost"
            size="sm"
          >
            {collapsed ? icons.chevronRight : icons.chevronLeft}
          </IconButton>
        </div>

        {/* Main navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1" aria-label="Main navigation">
          {navigation.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  'flex items-center gap-3 px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200',
                  isActive
                    ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                    : 'text-surface-500 hover:text-surface-700 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-200 dark:hover:bg-surface-800',
                  collapsed && 'justify-center px-2'
                )}
                aria-current={isActive ? 'page' : undefined}
                title={collapsed ? item.name : undefined}
                onClick={onClose}
              >
                {icons[item.icon as keyof typeof icons]}
                {!collapsed && <span>{item.name}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Project sections */}
        {!collapsed && (
          <div className="px-3 pb-4 space-y-6 border-t border-surface-200 dark:border-surface-700 pt-4">
            {/* Quick actions */}
            <div>
              <Link
                href="/dashboard/editor"
                className="flex items-center gap-3 w-full px-3 py-2.5 text-sm font-medium text-surface-500 hover:text-surface-700 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-200 dark:hover:bg-surface-800 rounded-lg transition-colors"
                onClick={onClose}
              >
                {icons.plus}
                <span>New Project</span>
              </Link>
            </div>

            {/* Recent projects */}
            {recentProjects.length > 0 && (
              <div>
                <h3 className="px-3 mb-2 text-xs font-semibold text-surface-400 uppercase tracking-wider dark:text-surface-500">
                  Recent Projects
                </h3>
                <div className="space-y-1">
                  {recentProjects.map((project) => (
                    <Link
                      key={project.id}
                      href={`/dashboard/editor/${project.id}`}
                      className={cn(
                        'flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors truncate',
                        currentProject?.id === project.id
                          ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                          : 'text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-100 dark:hover:bg-surface-800'
                      )}
                      onClick={onClose}
                      title={project.name}
                    >
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-surface-100 dark:bg-surface-800 flex-shrink-0">
                        {icons.folder}
                      </div>
                      <span className="truncate flex-1 min-w-0">{project.name}</span>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Starred projects */}
            {starredProjects.length > 0 && (
              <div>
                <h3 className="px-3 mb-2 text-xs font-semibold text-surface-400 uppercase tracking-wider dark:text-surface-500">
                  Starred
                </h3>
                <div className="space-y-1">
                  {starredProjects.map((project) => (
                    <Link
                      key={project.id}
                      href={`/dashboard/editor/${project.id}`}
                      className={cn(
                        'flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors truncate',
                        currentProject?.id === project.id
                          ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                          : 'text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-100 dark:hover:bg-surface-800'
                      )}
                      onClick={onClose}
                      title={project.name}
                    >
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-yellow-100 dark:bg-yellow-900/30 flex-shrink-0">
                        {icons.star}
                      </div>
                      <span className="truncate flex-1 min-w-0">{project.name}</span>
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className={cn('border-t border-surface-200 dark:border-surface-700 p-3', collapsed && 'px-2')}>
          {!collapsed ? (
            <div className="flex items-center gap-3 px-3 py-2 text-sm text-surface-500 dark:text-surface-400">
              <div className="h-8 w-8 rounded-full bg-surface-100 dark:bg-surface-800 flex items-center justify-center flex-shrink-0">
                {icons.user}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-surface-700 dark:text-surface-300 truncate">John Doe</p>
                <p className="text-xs truncate">john@example.com</p>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center">
              <div className="h-8 w-8 rounded-full bg-surface-100 dark:bg-surface-800 flex items-center justify-center">
                {icons.user}
              </div>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}