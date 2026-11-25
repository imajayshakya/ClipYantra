'use client';

import { ReactNode } from 'react';
import { Plus, Video, Settings, LayoutDashboard } from '@/components/ui/icons';

export default function EditorLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="h-screen flex flex-col bg-surface-950">
      {/* Top toolbar */}
      <header className="flex h-14 items-center justify-between border-b border-surface-800 bg-surface-900/80 backdrop-blur-sm px-4">
        <div className="flex items-center gap-4">
          <a href="/dashboard" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600">
              <Video className="h-5 w-5 text-white" aria-hidden="true" />
            </div>
            <span className="text-heading-md font-bold text-white">ClipYantra Editor</span>
          </a>
        </div>

        <div className="flex-1 max-w-xl mx-4" />

        <div className="flex items-center gap-2">
          <button className="btn-ghost btn-sm btn-icon text-surface-400 hover:text-white" aria-label="Project settings">
            <Settings className="h-4 w-4" aria-hidden="true" />
          </button>
          <button className="btn-primary btn-sm">
            <Plus className="h-4 w-4" aria-hidden="true" />
            <span>Export</span>
          </button>
        </div>
      </header>

      {/* Editor workspace */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left sidebar - Media/Transcript */}
        <aside className="hidden lg:flex lg:w-72 flex-col border-r border-surface-800 bg-surface-900">
          <nav className="flex h-12 border-b border-surface-800" aria-label="Editor panels">
            <button className="flex-1 flex items-center justify-center gap-2 rounded-none border-b-2 border-brand-500 bg-transparent px-3 py-2 text-body-sm font-medium text-white transition-colors" aria-current="true">
              <LayoutDashboard className="h-4 w-4" aria-hidden="true" />
              <span>Timeline</span>
            </button>
            <button className="flex-1 flex items-center justify-center gap-2 rounded-none border-b-2 border-transparent bg-transparent px-3 py-2 text-body-sm font-medium text-surface-500 hover:text-surface-300 hover:border-surface-700 transition-colors">
              <Video className="h-4 w-4" aria-hidden="true" />
              <span>Media</span>
            </button>
          </nav>
          <div className="flex-1 overflow-y-auto p-4">
            <div className="space-y-4">
              <p className="text-body-sm text-surface-500">Timeline panel - clips, tracks, edits</p>
            </div>
          </div>
        </aside>

        {/* Center - Preview */}
        <main className="flex-1 flex flex-col min-w-0">
          <div className="flex-1 flex items-center justify-center relative">
            <div className="aspect-video max-w-full max-h-full bg-surface-900 rounded-none">
              <div className="flex h-full items-center justify-center">
                <Video className="h-16 w-16 text-surface-600" aria-hidden="true" />
              </div>
            </div>
          </div>

          {/* Timeline */}
          <div className="h-64 border-t border-surface-800 bg-surface-900">
            <div className="flex h-full items-center justify-center text-surface-500">
              <p className="text-body-md">Timeline - tracks, keyframes, clips</p>
            </div>
          </div>
        </main>

        {/* Right sidebar - Inspector */}
        <aside className="hidden lg:flex lg:w-72 flex-col border-l border-surface-800 bg-surface-900">
          <div className="flex h-12 items-center justify-between border-b border-surface-800 px-4">
            <h2 className="text-body-sm font-medium text-white">Inspector</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            <p className="text-body-sm text-surface-500">Inspector panel - clip properties, effects, captions</p>
          </div>
        </aside>
      </div>
    </div>
  );
}