'use client';

import { useState } from 'react';
import { 
  FolderKanban, 
  Search, 
  Filter, 
  Plus, 
  Video, 
  MoreVertical, 
  Trash2, 
  Edit, 
  Copy, 
  Download,
  StatusBadge 
} from '@/components/ui/icons';

const projects = [
  { id: '1', name: 'Podcast Episode #42', status: 'completed', clips: 8, duration: '45:32', size: '2.4 GB', created: '2024-01-15', updated: '2 hours ago' },
  { id: '2', name: 'Webinar: AI in 2024', status: 'processing', clips: 0, duration: '1:23:15', size: '5.1 GB', created: '2024-01-14', updated: '5 hours ago' },
  { id: '3', name: 'Product Launch Video', status: 'draft', clips: 3, duration: '12:45', size: '890 MB', created: '2024-01-13', updated: '1 day ago' },
  { id: '4', name: 'Tutorial Series', status: 'completed', clips: 15, duration: '2:15:30', size: '8.2 GB', created: '2024-01-12', updated: '3 days ago' },
  { id: '5', name: 'Interview with CEO', status: 'completed', clips: 5, duration: '38:22', size: '1.8 GB', created: '2024-01-11', updated: '1 week ago' },
  { id: '6', name: 'Conference Keynote', status: 'failed', clips: 0, duration: '55:10', size: '3.2 GB', created: '2024-01-10', updated: '1 week ago' },
];

export default function LibraryPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('list');

  const filteredProjects = projects.filter((project) => {
    const matchesSearch = project.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || project.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-display-sm font-bold text-text-primary">Library</h1>
          <p className="mt-1 text-body-md text-text-secondary">
            Manage all your video projects and generated clips
          </p>
        </div>
        <a href="/dashboard/editor/new" className="btn-primary">
          <Plus className="h-4 w-4" aria-hidden="true" />
          <span>New Project</span>
        </a>
      </div>

      {/* Toolbar */}
      <div className="card p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" aria-hidden="true" />
            <input
              type="search"
              placeholder="Search projects..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input pl-10"
              aria-label="Search projects"
            />
          </div>

          <div className="flex items-center gap-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input w-auto"
              aria-label="Filter by status"
            >
              <option value="all">All Status</option>
              <option value="completed">Completed</option>
              <option value="processing">Processing</option>
              <option value="draft">Draft</option>
              <option value="failed">Failed</option>
            </select>

            <div className="flex items-center border-l border-border-default pl-4 ml-2" role="group" aria-label="View mode">
              <button
                onClick={() => setViewMode('list')}
                className={clsx(
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'list' ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/50 dark:text-brand-300' : 'text-text-muted hover:bg-surface-100'
                )}
                aria-pressed={viewMode === 'list'}
                aria-label="List view"
              >
                <FolderKanban className="h-5 w-5" aria-hidden="true" />
              </button>
              <button
                onClick={() => setViewMode('grid')}
                className={clsx(
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'grid' ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/50 dark:text-brand-300' : 'text-text-muted hover:bg-surface-100'
                )}
                aria-pressed={viewMode === 'grid'}
                aria-label="Grid view"
              >
                <Filter className="h-5 w-5" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Projects list */}
      <div className="card overflow-hidden">
        {viewMode === 'list' ? (
          <div className="overflow-x-auto">
            <table className="w-full" role="table">
              <thead>
                <tr className="border-b border-border-default bg-surface-50/50">
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Project</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Status</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Clips</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Duration</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Size</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Created</th>
                  <th className="text-left px-6 py-4 text-body-sm font-medium text-text-secondary">Updated</th>
                  <th className="text-right px-6 py-4 text-body-sm font-medium text-text-secondary">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-default">
                {filteredProjects.map((project) => (
                  <tr key={project.id} className="hover:bg-surface-50/50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-4">
                        <div className="h-12 w-12 rounded-lg bg-brand-100 flex items-center justify-center flex-shrink-0 dark:bg-brand-900/50">
                          <Video className="h-6 w-6 text-brand-600 dark:text-brand-400" aria-hidden="true" />
                        </div>
                        <div>
                          <p className="text-body-md font-medium text-text-primary">{project.name}</p>
                          <p className="text-body-xs text-text-muted">ID: {project.id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={clsx(
                        'badge',
                        project.status === 'completed' && 'badge-success',
                        project.status === 'processing' && 'badge-warning',
                        project.status === 'draft' && 'badge-neutral',
                        project.status === 'failed' && 'badge-error'
                      )}>
                        {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-body-md text-text-primary">{project.clips}</td>
                    <td className="px-6 py-4 text-body-md text-text-secondary">{project.duration}</td>
                    <td className="px-6 py-4 text-body-md text-text-secondary">{project.size}</td>
                    <td className="px-6 py-4 text-body-sm text-text-muted">{project.created}</td>
                    <td className="px-6 py-4 text-body-sm text-text-muted">{project.updated}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-1">
                        <button
                          className="btn-ghost btn-sm btn-icon"
                          aria-label={`Edit ${project.name}`}
                        >
                          <Edit className="h-4 w-4" aria-hidden="true" />
                        </button>
                        <button
                          className="btn-ghost btn-sm btn-icon"
                          ariaLabel={`Duplicate ${project.name}`}
                        >
                          <Copy className="h-4 w-4" aria-hidden="true" />
                        </button>
                        {project.status === 'completed' && (
                          <button
                            className="btn-ghost btn-sm btn-icon"
                            aria-label={`Download clips for ${project.name}`}
                          >
                            <Download className="h-4 w-4" aria-hidden="true" />
                          </button>
                        )}
                        <div className="relative">
                          <button
                            className="btn-ghost btn-sm btn-icon"
                            aria-label={`More options for ${project.name}`}
                            aria-expanded="false"
                            aria-haspopup="true"
                          >
                            <MoreVertical className="h-4 w-4" aria-hidden="true" />
                          </button>
                        </div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {filteredProjects.map((project) => (
              <article
                key={project.id}
                className="card p-4 hover:shadow-lg transition-shadow duration-fast group"
              >
                <div className="aspect-video rounded-lg bg-surface-100 relative overflow-hidden mb-4 dark:bg-surface-800">
                  <Video className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-10 w-10 text-surface-400" aria-hidden="true" />
                  {project.status === 'processing' && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/50">
                      <div className="h-8 w-8 animate-spin rounded-full border-2 border-white border-t-transparent" aria-label="Processing" />
                    </div>
                  )}
                  {project.status === 'failed' && (
                    <div className="absolute inset-0 flex items-center justify-center bg-red-500/80">
                      <span className="text-white font-medium">Failed</span>
                    </div>
                  )}
                </div>
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0 flex-1">
                    <h3 className="text-body-md font-semibold text-text-primary truncate">{project.name}</h3>
                    <div className="mt-1 flex flex-wrap items-center gap-2 text-body-xs text-text-muted">
                      <span>{project.clips} clips</span>
                      <span>·</span>
                      <span>{project.duration}</span>
                      <span>·</span>
                      <span>{project.size}</span>
                    </div>
                  </div>
                  <span className={clsx(
                    'badge flex-shrink-0',
                    project.status === 'completed' && 'badge-success',
                    project.status === 'processing' && 'badge-warning',
                    project.status === 'draft' && 'badge-neutral',
                    project.status === 'failed' && 'badge-error'
                  )}>
                    {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
                  </span>
                </div>
                <div className="mt-3 flex items-center justify-end gap-1">
                  <button className="btn-ghost btn-sm btn-icon" aria-label={`Edit ${project.name}`}>
                    <Edit className="h-4 w-4" aria-hidden="true" />
                  </button>
                  <button className="btn-ghost btn-sm btn-icon" aria-label={`More options for ${project.name}`}>
                    <MoreVertical className="h-4 w-4" aria-hidden="true" />
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}

        {filteredProjects.length === 0 && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <FolderKanban className="h-12 w-12 text-surface-300 dark:text-surface-600 mb-4" aria-hidden="true" />
            <h3 className="text-heading-md font-semibold text-text-primary mb-2">No projects found</h3>
            <p className="text-body-md text-text-secondary mb-6 max-w-sm">
              {searchQuery || statusFilter !== 'all'
                ? 'Try adjusting your search or filter criteria.'
                : 'Get started by creating your first project.'}
            </p>
            <a href="/dashboard/editor/new" className="btn-primary">
              <Plus className="h-4 w-4" aria-hidden="true" />
              <span>Create Project</span>
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

import { useState } from 'react';
import { clsx } from 'clsx';