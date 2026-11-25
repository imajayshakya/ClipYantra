'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Volume2, 
  VolumeX, 
  Maximize, 
  Minimize,
  Settings
} from 'lucide-react';

interface PreviewProps {
  className?: string;
  src?: string;
  poster?: string;
  currentTime: number;
  duration: number;
  playing: boolean;
  volume: number;
  muted: boolean;
  playbackRate: number;
  fullscreen: boolean;
  onPlay: () => void;
  onPause: () => void;
  onSeek: (time: number) => void;
  onVolumeChange: (volume: number) => void;
  onMuteToggle: () => void;
  onPlaybackRateChange: (rate: number) => void;
  onFullscreenToggle: () => void;
  onFrameBack: () => void;
  onFrameForward: () => void;
}

export function Preview({
  className,
  src,
  poster,
  currentTime,
  duration,
  playing,
  volume,
  muted,
  playbackRate,
  fullscreen,
  onPlay,
  onPause,
  onSeek,
  onVolumeChange,
  onMuteToggle,
  onPlaybackRateChange,
  onFullscreenToggle,
  onFrameBack,
  onFrameForward,
}: PreviewProps) {
  const videoRef = React.useRef<HTMLVideoElement>(null);
  const [hovered, setHovered] = React.useState(false);
  const [showControls, setShowControls] = React.useState(false);
  const hideControlsTimeout = React.useRef<NodeJS.Timeout>();

  const formatTime = (time: number) => {
    const mins = Math.floor(time / 60);
    const secs = Math.floor(time % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleMouseMove = () => {
    setShowControls(true);
    if (hideControlsTimeout.current) {
      clearTimeout(hideControlsTimeout.current);
    }
    hideControlsTimeout.current = setTimeout(() => {
      setShowControls(false);
    }, 3000);
  };

  const handleVideoClick = () => {
    if (playing) onPause();
    else onPlay();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case ' ':
      case 'k':
        e.preventDefault();
        if (playing) onPause();
        else onPlay();
        break;
      case 'ArrowLeft':
        e.preventDefault();
        onSeek(Math.max(0, currentTime - 5));
        break;
      case 'ArrowRight':
        e.preventDefault();
        onSeek(Math.min(duration, currentTime + 5));
        break;
      case 'ArrowUp':
        e.preventDefault();
        onVolumeChange(Math.min(1, volume + 0.1));
        break;
      case 'ArrowDown':
        e.preventDefault();
        onVolumeChange(Math.max(0, volume - 0.1));
        break;
      case 'm':
        onMuteToggle();
        break;
      case 'f':
        onFullscreenToggle();
        break;
      case ',':
        onFrameBack();
        break;
      case '.':
        onFrameForward();
        break;
    }
  };

  React.useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    video.volume = muted ? 0 : volume;
    video.playbackRate = playbackRate;

    if (playing) {
      video.play().catch(() => {});
    } else {
      video.pause();
    }
  }, [playing, volume, muted, playbackRate]);

  return (
    <div
      className={cn(
        'relative bg-surface-900 rounded-lg overflow-hidden',
        'flex-1 flex flex-col',
        className
      )}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onMouseMove={handleMouseMove}
      role="region"
      aria-label="Video preview"
      tabIndex={0}
      onKeyDown={handleKeyDown}
    >
      {/* Video element */}
      <video
        ref={videoRef}
        src={src}
        poster={poster}
        className="w-full h-full object-contain flex-1"
        onClick={handleVideoClick}
        onTimeUpdate={(e) => onSeek(e.currentTarget.currentTime)}
        onLoadedMetadata={(e) => {}}
        onEnded={() => onPause()}
        playsInline
      />

      {/* Loading placeholder */}
      {!src && (
        <div className="absolute inset-0 flex items-center justify-center bg-surface-900">
          <div className="text-center text-surface-500">
            <svg className="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-lg">No video loaded</p>
            <p className="text-sm mt-1">Add media to the timeline to preview</p>
          </div>
        </div>
      )}

      {/* Controls overlay */}
      {(hovered || showControls || playing) && (
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 transition-opacity duration-200">
          {/* Progress bar */}
          <div className="mb-3">
            <div
              className="relative h-2 bg-surface-700 rounded-full cursor-pointer"
              role="slider"
              aria-label="Video progress"
              aria-valuemin={0}
              aria-valuemax={duration}
              aria-valuenow={currentTime}
              onClick={(e) => {
                const rect = e.currentTarget.getBoundingClientRect();
                const pos = (e.clientX - rect.left) / rect.width;
                onSeek(pos * duration);
              }}
              onMouseDown={(e) => {
                const handleDrag = (moveEvent: MouseEvent) => {
                  const rect = e.currentTarget.getBoundingClientRect();
                  const pos = Math.max(0, Math.min(1, (moveEvent.clientX - rect.left) / rect.width));
                  onSeek(pos * duration);
                };
                const handleUp = () => {
                  window.removeEventListener('mousemove', handleDrag);
                  window.removeEventListener('mouseup', handleUp);
                };
                window.addEventListener('mousemove', handleDrag);
                window.addEventListener('mouseup', handleUp);
              }}
            >
              {/* Buffered */}
              <div
                className="absolute top-0 bottom-0 bg-brand-500/30 rounded-full"
                style={{ width: '100%' }}
              />
              {/* Played */}
              <div
                className="absolute top-0 bottom-0 bg-brand-500 rounded-full"
                style={{ width: `${duration > 0 ? (currentTime / duration) * 100 : 0}%` }}
              />
              {/* Playhead handle */}
              <div
                className="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg transform transition-transform duration-75"
                style={{ left: `${duration > 0 ? (currentTime / duration) * 100 : 0}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-surface-400 mt-1 font-mono">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>
          </div>

          {/* Control buttons */}
          <div className="flex items-center justify-between gap-4">
            {/* Left controls */}
            <div className="flex items-center gap-1">
              <button
                onClick={onFrameBack}
                className="p-2 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                aria-label="Previous frame (,)"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 18l-6-6 6-6" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18l-6-6 6-6" />
                </svg>
              </button>
              <button
                onClick={() => onSeek(Math.max(0, currentTime - 10))}
                className="p-2 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                aria-label="Rewind 10s (←)"
              >
                <SkipBack className="h-5 w-5" />
              </button>
              <button
                onClick={() => playing ? onPause() : onPlay()}
                className="p-3 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                aria-label={playing ? 'Pause (Space)' : 'Play (Space)'}
              >
                {playing ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
              </button>
              <button
                onClick={() => onSeek(Math.min(duration, currentTime + 10))}
                className="p-2 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                aria-label="Forward 10s (→)"
              >
                <SkipForward className="h-5 w-5" />
              </button>
              <button
                onClick={onFrameForward}
                className="p-2 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                aria-label="Next frame (.)"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 6l6 6-6 6" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 6l6 6-6 6" />
                </svg>
              </button>
            </div>

            {/* Center - Time display */}
            <div className="flex items-center gap-2 text-sm text-surface-200 font-mono">
              <span>{formatTime(currentTime)} / {formatTime(duration)}</span>
            </div>

            {/* Right controls */}
            <div className="flex items-center gap-2">
              {/* Volume */}
              <div className="relative flex items-center gap-2">
                <button
                  onClick={onMuteToggle}
                  className="p-2 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                  aria-label={muted ? 'Unmute (M)' : 'Mute (M)'}
                >
                  {muted || volume === 0 ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
                </button>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={muted ? 0 : volume}
                  onChange={(e) => onVolumeChange(parseFloat(e.target.value))}
                  className="w-24 h-1 bg-surface-700 rounded-lg appearance-none cursor-pointer accent-brand-500"
                  aria-label="Volume"
                />
              </div>

              {/* Playback rate */}
              <select
                value={playbackRate}
                onChange={(e) => onPlaybackRateChange(parseFloat(e.target.value))}
                className="px-2 py-1 text-sm text-surface-200 bg-surface-800 border border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
                aria-label="Playback speed"
              >
                {[0.25, 0.5, 0.75, 1, 1.25, 1.5, 2].map((rate) => (
                  <option key={rate} value={rate}>{rate}x</option>
                ))}
              </select>

              {/* Fullscreen */}
              <button
                onClick={onFullscreenToggle}
                className="p-2 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                aria-label={fullscreen ? 'Exit fullscreen (F)' : 'Enter fullscreen (F)'}
              >
                {fullscreen ? <Minimize className="h-5 w-5" /> : <Maximize className="h-5 w-5" />}
              </button>

              {/* Settings */}
              <button
                className="p-2 text-surface-200 hover:text-white transition-colors rounded-lg hover:bg-surface-700"
                aria-label="Settings"
              >
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}