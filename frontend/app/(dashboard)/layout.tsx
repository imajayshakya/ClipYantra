'use client';

import { ReactNode, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { clsx } from 'clsx';
import {
  LayoutDashboard,
  FolderKanban,
  Settings,
  Menu,
  X,
  ChevronLeft,
  ChevronRight,
  LogOut,
  User,
  Bell,
  Search,
  ClipYantraLogo,
} from '@/components/ui/icons';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Library', href: '/dashboard/library', icon: FolderKanban },
  { name: 'Editor', href: '/dashboard/editor', icon: ClipYantraLogo },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
];

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className="min-h-screen bg-background-secondary flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={clsx(
          'fixed lg:relative z-50 flex h-full flex-col transition-all duration-fast bg-background-primary border-r border-border-default',
          sidebarCollapsed ? 'w-16' : 'w-64',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
        aria-label="Main navigation"
      >
        {/* Sidebar header */}
        <div className={clsx('flex h-16 items-center border-b border-border-default px-4', sidebarCollapsed && 'justify-center')}>
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="mr-auto flex h-10 w-10 items-center justify-center rounded-lg text-text-secondary hover:bg-surface-100 hover:text-text-primary transition-colors lg:hidden"
            aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            aria-expanded={!sidebarCollapsed}
          >
            {sidebarCollapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
          </button>

          <Link href="/dashboard" className="flex items-center gap-2" aria-label="ClipYantra Home">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600">
              <ClipYantraLogo className="h-5 w-5 text-white" aria-hidden="true" />
            </div>
            {!sidebarCollapsed && (
              <span className="text-heading-md font-bold text-text-primary">ClipYantra</span>
            )}
          </Link>

          <button
            onClick={() => setSidebarOpen(false)}
            className="ml-auto flex h-10 w-10 items-center justify-center rounded-lg text-text-secondary hover:bg-surface-100 hover:text-text-primary transition-colors lg:hidden"
            aria-label="Close sidebar"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-1" aria-label="Main">
          <ul className="space-y-1" role="list">
            {navigation.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={clsx(
                      'flex items-center gap-3 rounded-lg px-3 py-2.5 text-body-sm font-medium transition-all duration-fast',
                      isActive
                        ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/50 dark:text-brand-300'
                        : 'text-text-secondary hover:bg-surface-100 hover:text-text-primary',
                      sidebarCollapsed && 'justify-center px-2'
                    )}
                    aria-current={isActive ? 'page' : undefined}
                    title={sidebarCollapsed ? item.name : undefined}
                  >
                    <item.icon className="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                    {!sidebarCollapsed && <span>{item.name}</span>}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Sidebar footer */}
        <div className={clsx('border-t border-border-default p-4', sidebarCollapsed && 'hidden')}>
          <div className="flex items-center gap-3 rounded-lg px-3 py-2">
            <div className="h-9 w-9 rounded-full bg-brand-100 flex items-center justify-center flex-shrink-0">
              <User className="h-5 w-5 text-brand-600" aria-hidden="true" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-body-sm font-medium text-text-primary truncate">John Doe</p>
              <p className="text-body-xs text-text-muted truncate">john@clipyantra.com</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 lg:ml-0">
        {/* Top header */}
        <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-border-default bg-background-primary/80 backdrop-blur-sm px-4 lg:px-6">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden flex h-10 w-10 items-center justify-center rounded-lg text-text-secondary hover:bg-surface-100 hover:text-text-primary transition-colors"
            aria-label="Open navigation menu"
          >
            <Menu className="h-5 w-5" />
          </button>

          <div className="flex-1" />

          <div className="flex items-center gap-2">
            {/* Search */}
            <div className="relative hidden sm:block">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" aria-hidden="true" />
              <input
                type="search"
                placeholder="Search projects..."
                className="input pl-10 w-64 sm:w-80"
                aria-label="Search projects"
              />
            </div>

            {/* Notifications */}
            <button
              className="relative flex h-10 w-10 items-center justify-center rounded-lg text-text-secondary hover:bg-surface-100 hover:text-text-primary transition-colors"
              aria-label="Notifications"
            >
              <Bell className="h-5 w-5" />
              <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-error" aria-label="3 unread notifications" />
            </button>

            {/* User menu */}
            <div className="relative">
              <button
                className="flex items-center gap-2 rounded-lg px-3 py-1.5 hover:bg-surface-100 transition-colors"
                aria-label="User menu"
                aria-expanded="false"
                aria-haspopup="true"
              >
                <div className="h-8 w-8 rounded-full bg-brand-100 flex items-center justify-center">
                  <User className="h-5 w-5 text-brand-600" aria-hidden="true" />
                </div>
                <span className="hidden sm:block text-body-sm font-medium text-text-primary">John Doe</span>
                <ChevronLeft className="h-4 w-4 text-text-muted" />
              </button>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-4 lg:p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}

// ClipYantra logo component
function ClipYantraLogo({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <rect width="32" height="32" rx="8" fill="currentColor" />
      <path
        d="M10 10h12v12H10z"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M14 14h4v4h-4z"
        fill="white"
      />
    </svg>
  );
}