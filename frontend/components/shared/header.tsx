'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Button, IconButton } from '@/components/ui';
import { useUserStore } from '@/store';

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
  menu: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
  ),
  x: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
  ),
  chevronDown: (
    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
  ),
  bell: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
  ),
  user: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
  ),
  logOut: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
  ),
  sun: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
  ),
  moon: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
  ),
  monitor: (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
  ),
};

export function Header() {
  const pathname = usePathname();
  const { user, logout } = useUserStore();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const [userMenuOpen, setUserMenuOpen] = React.useState(false);
  const [notificationsOpen, setNotificationsOpen] = React.useState(false);
  const userMenuRef = React.useRef<HTMLDivElement>(null);
  const notificationsRef = React.useRef<HTMLDivElement>(null);

  // Close menus on outside click
  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setUserMenuOpen(false);
      }
      if (notificationsRef.current && !notificationsRef.current.contains(event.target as Node)) {
        setNotificationsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleThemeToggle = () => {
    const html = document.documentElement;
    const currentTheme = html.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.classList.toggle('dark');
    localStorage.setItem('theme', newTheme);
    useUserStore.getState().updatePreferences({ theme: newTheme as 'light' | 'dark' | 'system' });
  };

  const isDark = document.documentElement.classList.contains('dark');

  return (
    <header className="sticky top-0 z-40 w-full border-b border-surface-200 bg-surface-50/80 backdrop-blur-sm dark:border-surface-700 dark:bg-surface-900/80">
      <div className="flex h-16 items-center justify-between px-4 gap-4">
        {/* Mobile menu button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="lg:hidden p-2 text-surface-500 hover:text-surface-700 dark:text-surface-400 dark:hover:text-surface-200 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800"
          aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={mobileMenuOpen}
        >
          {mobileMenuOpen ? icons.x : icons.menu}
        </button>

        {/* Logo */}
        <Link href="/dashboard" className="flex items-center gap-2 lg:ml-4" aria-label="ClipYantra Dashboard">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600">
            <svg className="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span className="hidden font-bold text-xl text-surface-900 dark:text-white lg:block">ClipYantra</span>
        </Link>

        {/* Desktop navigation */}
        <nav className="hidden lg:flex lg:items-center lg:gap-1 lg:flex-1 lg:justify-center" aria-label="Main navigation">
          {navigation.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  'flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200',
                  isActive
                    ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                    : 'text-surface-500 hover:text-surface-700 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-200 dark:hover:bg-surface-800'
                )}
                aria-current={isActive ? 'page' : undefined}
              >
                {icons[item.icon as keyof typeof icons]}
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Right side actions */}
        <div className="flex items-center gap-2">
          {/* Theme toggle */}
          <button
            onClick={handleThemeToggle}
            className="p-2 text-surface-500 hover:text-surface-700 dark:text-surface-400 dark:hover:text-surface-200 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800"
            aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {isDark ? icons.sun : icons.moon}
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setNotificationsOpen(!notificationsOpen)}
              className="relative p-2 text-surface-500 hover:text-surface-700 dark:text-surface-400 dark:hover:text-surface-200 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800"
              aria-label="Notifications"
              aria-expanded={notificationsOpen}
            >
              {icons.bell}
              <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500" aria-hidden="true" />
            </button>

            {notificationsOpen && (
              <div
                ref={notificationsRef}
                className="absolute right-0 mt-2 w-80 rounded-xl border border-surface-200 bg-surface-50 p-4 shadow-lg dark:border-surface-700 dark:bg-surface-800"
                role="menu"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-surface-900 dark:text-surface-100">Notifications</h3>
                  <button className="text-sm text-brand-600 hover:underline">Mark all read</button>
                </div>
                <div className="space-y-3 max-h-80 overflow-y-auto">
                  {[
                    { title: 'Export completed', description: 'Your video export is ready to download', time: '2 min ago', unread: true },
                    { title: 'New comment', description: 'John commented on "Summer Campaign"', time: '1 hour ago', unread: true },
                    { title: 'Transcription ready', description: 'Auto-captions generated for your project', time: '3 hours ago', unread: false },
                  ].map((notification, index) => (
                    <button
                      key={index}
                      className={cn(
                        'w-full text-left p-3 rounded-lg transition-colors',
                        notification.unread ? 'bg-brand-50 dark:bg-brand-900/30' : 'hover:bg-surface-100 dark:hover:bg-surface-700'
                      )}
                      role="menuitem"
                    >
                      <p className={cn('font-medium text-sm', notification.unread ? 'text-surface-900 dark:text-surface-100' : 'text-surface-700 dark:text-surface-300')}>
                        {notification.title}
                      </p>
                      <p className="mt-0.5 text-sm text-surface-500 dark:text-surface-400">{notification.description}</p>
                      <p className="mt-1 text-xs text-surface-400 dark:text-surface-500">{notification.time}</p>
                    </button>
                  ))}
                </div>
                <button className="mt-4 w-full text-center text-sm text-brand-600 hover:underline">View all notifications</button>
              </div>
            )}
          </div>

          {/* User menu */}
          <div className="relative" ref={userMenuRef}>
            <button
              onClick={() => setUserMenuOpen(!userMenuOpen)}
              className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
              aria-label="User menu"
              aria-expanded={userMenuOpen}
            >
              <div className="h-8 w-8 rounded-full bg-brand-100 flex items-center justify-center">
                {icons.user}
              </div>
              <span className="hidden lg:block text-sm font-medium text-surface-700 dark:text-surface-300">
                {user?.name || 'User'}
              </span>
              {icons.chevronDown}
            </button>

            {userMenuOpen && (
              <div className="absolute right-0 mt-2 w-56 rounded-xl border border-surface-200 bg-surface-50 py-2 shadow-lg dark:border-surface-700 dark:bg-surface-800" role="menu">
                <div className="px-4 py-2 border-b border-surface-200 dark:border-surface-700">
                  <p className="text-sm font-medium text-surface-900 dark:text-surface-100">{user?.name || 'User'}</p>
                  <p className="text-xs text-surface-500 dark:text-surface-400 truncate">{user?.email}</p>
                </div>
                <Link
                  href="/dashboard/settings?tab=profile"
                  className="flex items-center gap-3 px-4 py-2 text-sm text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-700"
                  role="menuitem"
                  onClick={() => setUserMenuOpen(false)}
                >
                  {icons.user}
                  Profile
                </Link>
                <Link
                  href="/dashboard/settings?tab=account"
                  className="flex items-center gap-3 px-4 py-2 text-sm text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-700"
                  role="menuitem"
                  onClick={() => setUserMenuOpen(false)}
                >
                  {icons.settings}
                  Account Settings
                </Link>
                <hr className="my-2 border-surface-200 dark:border-surface-700" />
                <button
                  onClick={() => logout()}
                  className="flex w-full items-center gap-3 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-surface-100 dark:hover:bg-surface-700"
                  role="menuitem"
                >
                  {icons.logOut}
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile navigation drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-900 px-4 py-4">
          <nav className="flex flex-col gap-1" aria-label="Mobile navigation">
            {navigation.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    'flex items-center gap-3 px-3 py-2.5 text-base font-medium rounded-lg transition-colors',
                    isActive
                      ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                      : 'text-surface-500 hover:text-surface-700 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-200 dark:hover:bg-surface-800'
                  )}
                  aria-current={isActive ? 'page' : undefined}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {icons[item.icon as keyof typeof icons]}
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      )}

      {/* Backdrop for mobile menu */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}
    </header>
  );
}