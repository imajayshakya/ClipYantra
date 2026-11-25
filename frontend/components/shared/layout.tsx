'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Header } from './header';
import { Sidebar } from './sidebar';
import { useProjectStore } from '@/store';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const { sidebarOpen, setSidebarOpen } = useProjectStore();
  const [collapsed, setCollapsed] = React.useState(false);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
  const toggleCollapse = () => setCollapsed(!collapsed);

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-950">
      {/* Header */}
      <Header />

      <div className="flex">
        {/* Sidebar */}
        <Sidebar
          open={sidebarOpen}
          onClose={toggleSidebar}
          collapsed={collapsed}
          onToggleCollapse={toggleCollapse}
        />

        {/* Main content */}
        <main
          className={cn(
            'flex-1 min-w-0 transition-all duration-300',
            collapsed ? 'lg:ml-20' : 'lg:ml-64'
          )}
        >
          <div className="p-4 lg:p-6 xl:p-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

// Editor layout with three-panel structure
interface EditorLayoutProps {
  children: React.ReactNode;
  leftPanel?: React.ReactNode;
  centerPanel?: React.ReactNode;
  rightPanel?: React.ReactNode;
  leftPanelOpen?: boolean;
  rightPanelOpen?: boolean;
  onToggleLeftPanel?: () => void;
  onToggleRightPanel?: () => void;
}

export function EditorLayout({
  children,
  leftPanel,
  centerPanel,
  rightPanel,
  leftPanelOpen = true,
  rightPanelOpen = true,
  onToggleLeftPanel,
  onToggleRightPanel,
}: EditorLayoutProps) {
  const { sidebarOpen, setSidebarOpen } = useProjectStore();
  const [collapsed, setCollapsed] = React.useState(false);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
  const toggleCollapse = () => setCollapsed(!collapsed);

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-950 flex flex-col">
      {/* Header */}
      <Header />

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          open={sidebarOpen}
          onClose={toggleSidebar}
          collapsed={collapsed}
          onToggleCollapse={toggleCollapse}
        />

        {/* Editor workspace */}
        <div className={cn(
          'flex-1 flex flex-col overflow-hidden transition-all duration-300',
          collapsed ? 'lg:ml-20' : 'lg:ml-64'
        )}>
          {/* Top toolbar */}
          <div className="flex h-12 items-center justify-between px-4 border-b border-surface-200 bg-surface-50 dark:border-surface-700 dark:bg-surface-900">
            <div className="flex items-center gap-4">
              <button
                onClick={toggleSidebar}
                className="lg:hidden p-2 text-surface-500 hover:text-surface-700 dark:text-surface-400 dark:hover:text-surface-200 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800"
                aria-label="Open sidebar"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
              </button>
              <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-100">Clip Studio</h1>
            </div>
            <div className="flex items-center gap-2">
              <button className="p-2 text-surface-500 hover:text-surface-700 dark:text-surface-400 dark:hover:text-surface-200 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800" aria-label="Save">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
              </button>
              <button className="p-2 text-surface-500 hover:text-surface-700 dark:text-surface-400 dark:hover:text-surface-200 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800" aria-label="Export">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
              </button>
            </div>
          </div>

          {/* Three-panel layout */}
          <div className="flex-1 flex overflow-hidden">
            {/* Left panel - Media/Transcript/Clips */}
            {leftPanelOpen && (
              <aside
                className={cn(
                  'flex flex-col border-r border-surface-200 bg-surface-50 dark:border-surface-700 dark:bg-surface-900 transition-all duration-300 overflow-hidden',
                  'w-80 flex-shrink-0'
                )}
                aria-label="Media and transcript panel"
              >
                <div className="flex-1 flex flex-col overflow-hidden">
                  {leftPanel}
                </div>
              </aside>
            )}

            {/* Center panel - Preview/Timeline */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
              {centerPanel}
            </div>

            {/* Right panel - Inspector */}
            {rightPanelOpen && (
              <aside
                className={cn(
                  'flex flex-col border-l border-surface-200 bg-surface-50 dark:border-surface-700 dark:bg-surface-900 transition-all duration-300 overflow-hidden',
                  'w-80 flex-shrink-0'
                )}
                aria-label="Inspector panel"
              >
                <div className="flex-1 flex flex-col overflow-hidden">
                  {rightPanel}
                </div>
              </aside>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Auth layout for login/register pages
interface AuthLayoutProps {
  children: React.ReactNode;
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-950 flex">
      {/* Brand sidebar */}
      <aside className="hidden lg:flex lg:w-1/2 lg:min-h-screen bg-brand-600 flex-col items-center justify-center p-8 text-white">
        <div className="max-w-md">
          <div className="flex items-center gap-3 mb-12">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 backdrop-blur-sm">
              <svg className="h-7 w-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span className="text-2xl font-bold">ClipYantra</span>
          </div>
          <h2 className="text-4xl font-bold mb-6">Create stunning videos with AI</h2>
          <p className="text-lg text-white/80 mb-8">
            Transform your raw footage into professional clips. AI-powered editing, auto-captions, and smart scene detection make video creation effortless.
          </p>
          <div className="space-y-4">
            {[
              { icon: 'sparkles', text: 'AI-powered editing & auto-captions' },
              { icon: 'zap', text: 'Smart scene detection & highlights' },
              { icon: 'layers', text: 'Multi-track timeline editing' },
              { icon: 'cloud', text: 'Cloud rendering & collaboration' },
            ].map((feature, index) => (
              <div key={index} className="flex items-center gap-3 text-white/90">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/10">
                  {feature.icon === 'sparkles' && (
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M22 7v4M20 5h4M17 17v4m-2 2h4m-7-2v4m-2-2h4" /></svg>
                  )}
                  {feature.icon === 'zap' && (
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                  )}
                  {feature.icon === 'layers' && (
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
                  )}
                  {feature.icon === 'cloud' && (
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" /></svg>
                  )}
                </div>
                <span>{feature.text}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="absolute bottom-8 text-white/50 text-sm">
          Made with care for creators
        </div>
      </aside>

      {/* Form panel */}
      <main className="flex-1 flex items-center justify-center p-4 lg:p-12">
        <div className="w-full max-w-md">
          {children}
        </div>
      </main>
    </div>
  );
}