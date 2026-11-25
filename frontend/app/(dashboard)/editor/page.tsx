'use client';

import { Plus, Video, ArrowLeft } from '@/components/ui/icons';
import Link from 'next/link';

export default function EditorIndexPage() {
  return (
    <div className="h-screen flex flex-col bg-surface-950">
      {/* Top toolbar */}
      <header className="flex h-14 items-center justify-between border-b border-surface-800 bg-surface-900/80 backdrop-blur-sm px-4">
        <div className="flex items-center gap-4">
          <Link href="/dashboard" className="btn-ghost btn-sm btn-icon text-surface-400 hover:text-white" aria-label="Back to dashboard">
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          </Link>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600">
              <Video className="h-5 w-5 text-white" aria-hidden="true" />
            </div>
            <span className="text-heading-md font-bold text-white">ClipYantra Editor</span>
          </div>
        </div>

        <div className="flex-1" />

        <Link href="/dashboard/editor/new" className="btn-primary">
          <Plus className="h-4 w-4" aria-hidden="true" />
          <span>New Project</span>
        </Link>
      </header>

      {/* Project list */}
      <main className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-4xl">
          <div className="text-center mb-12">
            <h1 className="text-display-md font-bold text-white mb-4">Create a New Project</h1>
            <p className="text-body-lg text-surface-400">Upload a video to start generating clips with AI</p>
          </div>

          <div className="card bg-surface-900 border-surface-800 p-12 text-center">
            <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-brand-500/10">
              <Video className="h-8 w-8 text-brand-500" aria-hidden="true" />
            </div>
            <h2 className="mb-2 text-heading-lg font-semibold text-white">Drag & drop your video here</h2>
            <p className="mb-6 text-body-md text-surface-400">Or click to browse files</p>
            <input
              type="file"
              accept="video/*"
              className="sr-only"
              id="video-upload"
              aria-label="Upload video file"
            />
            <label
              htmlFor="video-upload"
              className="btn-outline inline-flex items-center gap-2 cursor-pointer"
            >
              <Video className="h-4 w-4" aria-hidden="true" />
              <span>Select Video File</span>
            </label>
            <p className="mt-4 text-body-sm text-surface-500">
              Supports MP4, MOV, AVI, MKV up to 10GB
            </p>
          </div>

          {/* Recent projects */}
          <section className="mt-12" aria-labelledby="recent-heading">
            <h2 id="recent-heading" className="mb-6 text-heading-lg font-semibold text-white">Recent Projects</h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {recentProjects.map((project) => (
                <Link
                  key={project.id}
                  href={`/dashboard/editor/${project.id}`}
                  className="card bg-surface-900 border-surface-800 overflow-hidden hover:border-brand-500/50 transition-colors group"
                >
                  <div className="aspect-video relative bg-surface-800">
                    <Video className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-10 w-10 text-surface-600 group-hover:text-brand-500 transition-colors" aria-hidden="true" />
                    {project.status === 'completed' && (
                      <div className="absolute bottom-2 right-2">
                        <span className="badge badge-success text-xs">{project.clips} clips</span>
                      </div>
                    )}
                  </div>
                  <div className="p-4">
                    <h3 className="font-medium text-white truncate group-hover:text-brand-400 transition-colors">{project.name}</h3>
                    <div className="mt-1 flex items-center gap-2 text-body-xs text-surface-500">
                      <span>{project.duration}</span>
                      <span>·</span>
                      <span>{project.updated}</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

const recentProjects = [
  { id: '1', name: 'Podcast Episode #42', status: 'completed', clips: 8, duration: '45:32', updated: '2 hours ago' },
  { id: '2', name: 'Webinar: AI in 2024', status: 'processing', clips: 0, duration: '1:23:15', updated: '5 hours ago' },
  { id: '3', name: 'Product Launch Video', status: 'draft', clips: 3, duration: '12:45', updated: '1 day ago' },
  { id: '4', name: 'Tutorial Series', status: 'completed', clips: 15, duration: '2:15:30', updated: '3 days ago' },
];