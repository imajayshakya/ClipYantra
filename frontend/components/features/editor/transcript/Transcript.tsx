'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Search, Filter, Mic, MicOff, Copy, Edit2 } from 'lucide-react';

interface TranscriptSegment {
  id: string;
  start: number;
  end: number;
  text: string;
  speaker?: string;
  confidence?: number;
  words?: Array<{
    word: string;
    start: number;
    end: number;
    confidence: number;
  }>;
}

interface TranscriptProps {
  className?: string;
  segments: TranscriptSegment[];
  currentTime: number;
  onSegmentClick: (segment: TranscriptSegment) => void;
  onSegmentEdit: (segment: TranscriptSegment) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  speakerFilter?: string;
  onSpeakerFilterChange: (speaker: string) => void;
  speakers: string[];
  editingSegmentId?: string;
  onSaveEdit: (segmentId: string, text: string) => void;
  onCancelEdit: () => void;
}

export function Transcript({
  className,
  segments,
  currentTime,
  onSegmentClick,
  onSegmentEdit,
  searchQuery,
  onSearchChange,
  speakerFilter,
  onSpeakerFilterChange,
  speakers,
  editingSegmentId,
  onSaveEdit,
  onCancelEdit,
}: TranscriptProps) {
  const formatTime = (time: number) => {
    const mins = Math.floor(time / 60);
    const secs = Math.floor(time % 60);
    const ms = Math.floor((time % 1) * 1000);
    return `${mins}:${secs.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`;
  };

  const filteredSegments = segments.filter((segment) => {
    const matchesSearch = segment.text.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSpeaker = !speakerFilter || segment.speaker === speakerFilter;
    return matchesSearch && matchesSpeaker;
  });

  const activeSegment = segments.find(
    (s) => currentTime >= s.start && currentTime <= s.end
  );

  return (
    <div className={cn('flex flex-col h-full bg-surface-50 dark:bg-surface-900', className)}>
      {/* Header */}
      <div className="p-4 border-b border-surface-200 dark:border-surface-700">
        <div className="flex items-center gap-4 mb-3">
          <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-100">
            Transcript
          </h2>
          <span className="px-2 py-0.5 text-xs font-medium bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 rounded-full">
            {segments.length} segments
          </span>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search transcript..."
            className="w-full pl-10 pr-4 py-2 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
            aria-label="Search transcript"
          />
        </div>

        {/* Speaker filter */}
        {speakers.length > 0 && (
          <div className="mt-3">
            <select
              value={speakerFilter || ''}
              onChange={(e) => onSpeakerFilterChange(e.target.value)}
              className="w-full px-3 py-2 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
              aria-label="Filter by speaker"
            >
              <option value="">All speakers</option>
              {speakers.map((speaker) => (
                <option key={speaker} value={speaker}>
                  {speaker}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Transcript list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {filteredSegments.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-surface-500">
            <Search className="h-12 w-12 mb-4 opacity-50" />
            <p className="text-lg">No transcript segments found</p>
            <p className="text-sm mt-1">Try adjusting your search or filter</p>
          </div>
        ) : (
          filteredSegments.map((segment) => (
            <TranscriptSegmentItem
              key={segment.id}
              segment={segment}
              isActive={activeSegment?.id === segment.id}
              isEditing={editingSegmentId === segment.id}
              formatTime={formatTime}
              onClick={() => onSegmentClick(segment)}
              onEdit={() => onSegmentEdit(segment)}
              onSave={(text) => onSaveEdit(segment.id, text)}
              onCancel={onCancelEdit}
            />
          ))
        )}
      </div>
    </div>
  );
}

interface TranscriptSegmentItemProps {
  segment: TranscriptSegment;
  isActive: boolean;
  isEditing: boolean;
  formatTime: (time: number) => string;
  onClick: () => void;
  onEdit: () => void;
  onSave: (text: string) => void;
  onCancel: () => void;
}

function TranscriptSegmentItem({
  segment,
  isActive,
  isEditing,
  formatTime,
  onClick,
  onEdit,
  onSave,
  onCancel,
}: TranscriptSegmentItemProps) {
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  React.useEffect(() => {
    if (isEditing && textareaRef.current) {
      textareaRef.current.focus();
      textareaRef.current.select();
    }
  }, [isEditing]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSave(e.currentTarget.value);
    } else if (e.key === 'Escape') {
      onCancel();
    }
  };

  if (isEditing) {
    return (
      <div className="bg-white dark:bg-surface-800 border-2 border-brand-500 rounded-lg p-3 animate-in fade-in slide-in-from-top-2 duration-150">
        <div className="flex items-start gap-3">
          <div className="flex-1 min-w-0">
            <textarea
              ref={textareaRef}
              value={segment.text}
              onChange={() => {}}
              onKeyDown={handleKeyDown}
              onBlur={() => onSave(textareaRef.current?.value || segment.text)}
              className="w-full px-3 py-2 text-sm bg-transparent border-0 focus:outline-none resize-none text-surface-900 dark:text-surface-100"
              rows={3}
              aria-label="Edit transcript segment"
            />
          </div>
          <div className="flex flex-col gap-1">
            <button
              onClick={() => onSave(textareaRef.current?.value || segment.text)}
              className="p-2 text-green-600 hover:bg-green-100 dark:hover:bg-green-900/30 rounded-lg transition-colors"
              aria-label="Save"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </button>
            <button
              onClick={onCancel}
              className="p-2 text-red-600 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg transition-colors"
              aria-label="Cancel"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div className="flex items-center gap-2 mt-2 text-xs text-surface-500 font-mono">
          <span>{formatTime(segment.start)} - {formatTime(segment.end)}</span>
          {segment.speaker && <span className="px-1.5 py-0.5 bg-surface-100 dark:bg-surface-700 rounded">{segment.speaker}</span>}
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        'bg-white dark:bg-surface-800 rounded-lg p-3 transition-all duration-150 cursor-pointer',
        'hover:bg-surface-50 dark:hover:bg-surface-700',
        'focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 dark:focus:ring-offset-surface-900',
        isActive && 'bg-brand-50 dark:bg-brand-900/20 border border-brand-200 dark:border-brand-800'
      )}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
      tabIndex={0}
      role="button"
      aria-label={`${segment.speaker || 'Segment'}: ${segment.text.substring(0, 50)}...`}
      aria-pressed={isActive}
    >
      <div className="flex items-start gap-3">
        <div className="flex-1 min-w-0">
          <p className="text-sm text-surface-900 dark:text-surface-100 leading-relaxed">
            {segment.text}
          </p>
          <div className="flex items-center gap-2 mt-2 text-xs text-surface-500 font-mono">
            <span>{formatTime(segment.start)} - {formatTime(segment.end)}</span>
            {segment.speaker && (
              <span className="flex items-center gap-1 px-2 py-0.5 bg-surface-100 dark:bg-surface-700 rounded-full">
                <Mic className="h-3 w-3" />
                {segment.speaker}
              </span>
            )}
            {segment.confidence !== undefined && (
              <span className={cn(
                'px-1.5 py-0.5 rounded',
                segment.confidence > 0.8 ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                segment.confidence > 0.5 ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300' :
                'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
              )}>
                {Math.round(segment.confidence * 100)}%
              </span>
            )}
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onEdit();
          }}
          className="p-1.5 text-surface-400 hover:text-surface-600 dark:hover:text-surface-300 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-700 flex-shrink-0"
          aria-label="Edit segment"
        >
          <Edit2 className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}