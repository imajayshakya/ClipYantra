'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

interface TimelineProps {
  className?: string;
  duration: number;
  playheadPosition: number;
  onPlayheadChange: (position: number) => void;
  tracks: any[];
  onTrackChange: (trackId: string, changes: any) => void;
  zoom: number;
  onZoomChange: (zoom: number) => void;
}

export function Timeline({
  className,
  duration,
  playheadPosition,
  onPlayheadChange,
  tracks,
  onTrackChange,
  zoom,
  onZoomChange,
}: TimelineProps) {
  return (
    <div
      className={cn('flex-1 overflow-auto bg-surface-900 relative', className)}
      role="region"
      aria-label="Video timeline"
      tabIndex={0}
    >
      <div className="flex min-w-max">
        {/* Time ruler */}
        <div className="w-12 border-r border-surface-700 flex-shrink-0">
          <div className="h-20 bg-surface-800 border-b border-surface-700 flex items-center justify-center">
            <span className="text-xs text-surface-400 font-mono">Time</span>
          </div>
          {tracks.map((track) => (
            <div key={track.id} className="h-40 border-b border-surface-700 flex items-center justify-center">
              <span className="text-xs text-surface-500">{track.name}</span>
            </div>
          ))}
        </div>

        {/* Timeline tracks */}
        <div className="flex-1 relative">
          {/* Time markers */}
          <div className="absolute top-0 left-0 right-0 h-20 bg-surface-800 border-b border-surface-700 pointer-events-none">
            {Array.from({ length: Math.ceil(duration / 10) }).map((_, i) => (
              <div
                key={i}
                className="absolute top-0 bottom-0 w-px bg-surface-600"
                style={{ left: `${(i * 10 / duration) * 100}%` }}
              />
            ))}
          </div>

          {/* Tracks */}
          <div className="relative">
            {tracks.map((track) => (
              <div
                key={track.id}
                className="h-40 border-b border-surface-700 relative"
              >
                {/* Track clips */}
                <div className="absolute inset-0 p-1">
                  {track.clips?.map((clip: any) => (
                    <div
                      key={clip.id}
                      className="absolute h-full rounded bg-brand-500/80 border border-brand-400 cursor-pointer hover:bg-brand-500 transition-colors"
                      style={{
                        left: `${(clip.start / duration) * 100}%`,
                        width: `${((clip.end - clip.start) / duration) * 100}%`,
                      }}
                      role="button"
                      tabIndex={0}
                      aria-label={`${clip.name}: ${clip.start}s - ${clip.end}s`}
                    >
                      <span className="text-xs text-white truncate block px-1">{clip.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Playhead */}
          <div
            className="absolute top-0 bottom-0 w-px bg-red-500 pointer-events-none z-10"
            style={{ left: `${(playheadPosition / duration) * 100}%` }}
            aria-hidden="true"
          >
            <div className="absolute top-0 left-[-4px] w-2 h-2 bg-red-500 rounded-full -translate-x-1/2 -translate-y-1/2" />
            <div className="absolute bottom-0 left-[-4px] w-2 h-2 bg-red-500 rounded-full -translate-x-1/2 translate-y-1/2" />
          </div>
        </div>
      </div>
    </div>
  );
}