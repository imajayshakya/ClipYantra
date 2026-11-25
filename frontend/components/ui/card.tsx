'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'outlined' | 'elevated' | 'filled';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hoverable?: boolean;
}

const cardStyles = {
  base: 'rounded-xl transition-all duration-200',
  variants: {
    default: 'bg-surface-50 border border-surface-200 dark:bg-surface-800 dark:border-surface-700',
    outlined: 'bg-transparent border-2 border-surface-200 dark:border-surface-700',
    elevated: 'bg-surface-50 shadow-lg dark:bg-surface-800',
    filled: 'bg-surface-100 border-0 dark:bg-surface-800/50',
  },
  padding: {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  },
  hoverable: 'hover:shadow-xl hover:-translate-y-0.5 cursor-pointer',
};

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', padding = 'md', hoverable = false, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          cardStyles.base,
          cardStyles.variants[variant],
          cardStyles.padding[padding],
          hoverable && cardStyles.hoverable,
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, title, description, action, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('flex items-start justify-between gap-4 mb-4', className)}
        {...props}
      >
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-surface-900 dark:text-surface-100 truncate">{title}</h3>
          {description && (
            <p className="mt-1 text-sm text-surface-500 dark:text-surface-400">{description}</p>
          )}
        </div>
        {action && <div className="flex-shrink-0">{action}</div>}
      </div>
    );
  }
);

CardHeader.displayName = 'CardHeader';

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ className, ...props }, ref) => {
    return (
      <div ref={ref} className={cn('', className)} {...props} />
    );
  }
);

CardContent.displayName = 'CardContent';

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  divided?: boolean;
}

export const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className, divided = true, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'flex items-center gap-3 mt-4 pt-4',
          divided && 'border-t border-surface-200 dark:border-surface-700',
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

CardFooter.displayName = 'CardFooter';

// Card preview for media/project thumbnails
export interface CardPreviewProps {
  src: string;
  alt?: string;
  aspectRatio?: '16:9' | '4:3' | '1:1' | '9:16';
  overlay?: React.ReactNode;
  badge?: React.ReactNode;
  onClick?: () => void;
}

export const CardPreview = React.forwardRef<HTMLDivElement, CardPreviewProps>(
  ({ className, src, alt, aspectRatio = '16:9', overlay, badge, onClick, ...props }, ref) => {
    const aspectRatios = {
      '16:9': 'aspect-video',
      '4:3': 'aspect-[4/3]',
      '1:1': 'aspect-square',
      '9:16': 'aspect-[9/16]',
    };

    return (
      <div
        ref={ref}
        className={cn('relative overflow-hidden rounded-lg', aspectRatios[aspectRatio], className)}
        onClick={onClick}
        role={onClick ? 'button' : undefined}
        tabIndex={onClick ? 0 : undefined}
        onKeyDown={onClick ? (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onClick(); }} : undefined}
        {...props}
      >
        <img
          src={src}
          alt={alt || ''}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
          loading="lazy"
        />
        {badge && (
          <div className="absolute top-2 left-2 z-10">{badge}</div>
        )}
        {overlay && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-200">
            {overlay}
          </div>
        )}
      </div>
    );
  }
);

CardPreview.displayName = 'CardPreview';

// Stat card for dashboard metrics
export interface StatCardProps {
  title: string;
  value: string | number;
  change?: {
    value: number;
    label: string;
    positive?: boolean;
  };
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
  loading?: boolean;
}

export const StatCard = ({ title, value, change, icon, trend = 'neutral', loading = false }: StatCardProps) => {
  const trendColors = {
    up: 'text-green-600 dark:text-green-400',
    down: 'text-red-600 dark:text-red-400',
    neutral: 'text-surface-500 dark:text-surface-400',
  };

  const trendIcons = {
    up: <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>,
    down: <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" /></svg>,
    neutral: <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" /></svg>,
  };

  if (loading) {
    return (
      <Card>
        <div className="space-y-3">
          <div className="h-4 w-3/4 animate-pulse bg-surface-200 dark:bg-surface-700 rounded" />
          <div className="h-8 w-1/2 animate-pulse bg-surface-200 dark:bg-surface-700 rounded" />
          {change && <div className="h-3 w-1/3 animate-pulse bg-surface-200 dark:bg-surface-700 rounded" />}
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-surface-500 dark:text-surface-400 truncate">{title}</p>
          <p className="mt-1 text-2xl font-bold text-surface-900 dark:text-surface-100">{value}</p>
          {change && (
            <div className="mt-2 flex items-center gap-1.5">
              <span className={cn('text-sm font-medium', trendColors[trend])}>
                {trendIcons[trend]}
                {change.value > 0 ? '+' : ''}{change.value}%
              </span>
              <span className="text-sm text-surface-500 dark:text-surface-400">{change.label}</span>
            </div>
          )}
        </div>
        {icon && <div className="flex-shrink-0 text-surface-400 dark:text-surface-500">{icon}</div>}
      </div>
    </Card>
  );
};

// Project card for library view
export interface ProjectCardProps {
  project: {
    id: string;
    name: string;
    description?: string;
    thumbnail?: string;
    aspectRatio: string;
    duration: number;
    status: string;
    updatedAt: string;
    tags: string[];
  };
  viewMode?: 'grid' | 'list';
  onClick?: () => void;
  onMenuClick?: (e: React.MouseEvent, projectId: string) => void;
}

export const ProjectCard = ({ project, viewMode = 'grid', onClick, onMenuClick }: ProjectCardProps) => {
  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hours > 0) return `${hours}h ${minutes}m`;
    if (minutes > 0) return `${minutes}m ${secs}s`;
    return `${secs}s`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const statusColors = {
    draft: 'bg-surface-200 text-surface-700 dark:bg-surface-700 dark:text-surface-300',
    processing: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    archived: 'bg-surface-100 text-surface-500 dark:bg-surface-800 dark:text-surface-400',
  };

  if (viewMode === 'list') {
    return (
      <Card variant="outlined" padding="sm" hoverable={!!onClick} onClick={onClick} className="flex items-center gap-4">
        {project.thumbnail && (
          <CardPreview src={project.thumbnail} alt={project.name} aspectRatio="16:9" className="w-24 h-14 flex-shrink-0" />
        )}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-medium text-surface-900 dark:text-surface-100 truncate">{project.name}</h3>
            <span className={cn('px-2 py-0.5 text-xs font-medium rounded-full', statusColors[project.status as keyof typeof statusColors] || statusColors.draft)}>
              {project.status}
            </span>
          </div>
          {project.description && <p className="mt-1 text-sm text-surface-500 dark:text-surface-400 truncate">{project.description}</p>}
          <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-surface-500 dark:text-surface-400">
            <span className="flex items-center gap-1">
              <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              {formatDuration(project.duration)}
            </span>
            <span className="flex items-center gap-1">
              <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
              {formatDate(project.updatedAt)}
            </span>
            <span className="flex items-center gap-1">
              <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
              {project.aspectRatio}
            </span>
          </div>
        </div>
        <button
          onClick={(e) => { e.stopPropagation(); onMenuClick?.(e, project.id); }}
          className="flex-shrink-0 p-2 text-surface-400 hover:text-surface-600 dark:hover:text-surface-300 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800"
          aria-label="More options"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" /></svg>
        </button>
      </Card>
    );
  }

  return (
    <Card variant="outlined" hoverable={!!onClick} onClick={onClick} className="group flex flex-col h-full">
      <div className="relative aspect-video overflow-hidden rounded-t-lg">
        {project.thumbnail ? (
          <img src={project.thumbnail} alt="" className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" loading="lazy" />
        ) : (
          <div className="w-full h-full bg-surface-200 dark:bg-surface-700 flex items-center justify-center">
            <svg className="h-12 w-12 text-surface-400 dark:text-surface-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
          </div>
        )}
        <div className="absolute top-2 right-2">
          <span className={cn('px-2 py-0.5 text-xs font-medium rounded-full', statusColors[project.status as keyof typeof statusColors] || statusColors.draft)}>
            {project.status}
          </span>
        </div>
        <button
          onClick={(e) => { e.stopPropagation(); onMenuClick?.(e, project.id); }}
          className="absolute top-2 left-2 p-1.5 text-surface-400 hover:text-white transition-colors rounded-lg opacity-0 group-hover:opacity-100 bg-black/30 hover:bg-black/50"
          aria-label="More options"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" /></svg>
        </button>
      </div>
      <div className="flex-1 p-4 flex flex-col">
        <h3 className="font-semibold text-surface-900 dark:text-surface-100 truncate">{project.name}</h3>
        {project.description && <p className="mt-1 text-sm text-surface-500 dark:text-surface-400 line-clamp-2">{project.description}</p>}
        <div className="mt-auto pt-3 flex flex-wrap items-center gap-2 text-xs text-surface-500 dark:text-surface-400">
          <span className="flex items-center gap-1">
            <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            {formatDuration(project.duration)}
          </span>
          <span className="flex items-center gap-1">
            <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            {formatDate(project.updatedAt)}
          </span>
        </div>
        {project.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {project.tags.slice(0, 3).map((tag) => (
              <span key={tag} className="px-2 py-0.5 text-xs font-medium rounded-full bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-300">
                {tag}
              </span>
            ))}
            {project.tags.length > 3 && (
              <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-surface-100 text-surface-500 dark:bg-surface-800 dark:text-surface-400">
                +{project.tags.length - 3}
              </span>
            )}
          </div>
        )}
      </div>
    </Card>
  );
};