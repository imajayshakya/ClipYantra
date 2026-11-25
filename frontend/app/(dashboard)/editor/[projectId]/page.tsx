'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { Video, Settings, LayoutDashboard, Scissors, FileText, Layers, Download, Play, Pause, Volume2, VolumeX, Maximize, Minimize } from '@/components/ui/icons';

export default function EditorProjectPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration] = useState(1800); // 30 minutes in seconds

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="h-screen flex flex-col bg-surface-950">
      {/* Top toolbar */}
      <header className="flex h-14 items-center justify-between border-b border-surface-800 bg-surface-900/80 backdrop-blur-sm px-4">
        <div className="flex items-center gap-4">
          <a href="/dashboard/editor" className="btn-ghost btn-sm btn-icon text-surface-400 hover:text-white" aria-label="Back to projects">
            <LayoutDashboard className="h-4 w-4" aria-hidden="true" />
          </a>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600">
              <Video className="h-5 w-5 text-white" aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-heading-md font-bold text-white">Project #{projectId}</h1>
              <p className="text-body-xs text-surface-500">Podcast Episode #42 · 8 clips generated</p>
            </div>
          </div>
        </div>

        <div className="flex-1 max-w-xl mx-4 flex items-center justify-center gap-2">
          <button className="btn-ghost btn-sm text-surface-400 hover:text-white" aria-label="Undo">
            <Scissors className="h-4 w-4" aria-hidden="true" />
          </button>
          <button className="btn-ghost btn-sm text-surface-400 hover:text-white" aria-label="Redo">
            <FileText className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button className="btn-ghost btn-sm text-surface-400 hover:text-white" aria-label="Project settings">
            <Settings className="h-4 w-4" aria-hidden="true" />
          </button>
          <button className="btn-primary btn-sm">
            <Download className="h-4 w-4" aria-hidden="true" />
            <span>Export</span>
          </button>
        </div>
      </header>

      {/* Editor workspace */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left sidebar - Media/Transcript/Clips */}
        <aside className="hidden lg:flex lg:w-72 flex-col border-r border-surface-800 bg-surface-900">
          <nav className="flex h-12 border-b border-surface-800" aria-label="Editor panels" role="tablist">
            {['Media', 'Transcript', 'Clips'].map((tab, index) => (
              <button
                key={tab}
                role="tab"
                aria-selected={index === 0}
                aria-controls={`panel-${tab.toLowerCase()}`}
                id={`tab-${tab.toLowerCase()}`}
                className={clsx(
                  'flex-1 flex items-center justify-center gap-2 rounded-none border-b-2 px-3 py-2 text-body-sm font-medium transition-colors',
                  index === 0
                    ? 'border-brand-500 bg-transparent text-white'
                    : 'border-transparent bg-transparent text-surface-500 hover:text-surface-300 hover:border-surface-700'
                )}
              >
                {index === 0 && <Layers className="h-4 w-4" aria-hidden="true" />}
                {index === 1 && <FileText className="h-4 w-4" aria-hidden="true" />}
                {index === 2 && <Scissors className="h-4 w-4" aria-hidden="true" />}
                <span>{tab}</span>
              </button>
            ))}
          </nav>
          <div className="flex-1 overflow-y-auto p-4" role="tabpanel" id="panel-media" aria-labelledby="tab-media">
            <div className="space-y-4">
              <div className="border border-surface-700 rounded-lg p-4">
                <p className="text-body-sm font-medium text-white mb-2">Source Video</p>
                <div className="aspect-video bg-surface-800 rounded relative overflow-hidden">
                  <Video className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-10 w-10 text-surface-600" aria-hidden="true" />
                </div>
                <p className="mt-2 text-body-xs text-surface-500">podcast-ep42.mp4 · 45:32 · 2.4 GB</p>
              </div>
              <div className="space-y-2">
                <p className="text-body-sm font-medium text-white">Generated Clips</p>
                {clips.map((clip) => (
                  <button
                    key={clip.id}
                    className="w-full flex items-center gap-3 p-2 rounded-lg bg-surface-800 hover:bg-surface-700 transition-colors text-left"
                  >
                    <div className="h-12 w-20 flex-shrink-0 bg-surface-700 rounded relative overflow-hidden">
                      <Video className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-5 w-5 text-surface-600" aria-hidden="true" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-body-sm font-medium text-white truncate">{clip.name}</p>
                      <p className="text-body-xs text-surface-500">{clip.duration} · {clip.aspectRatio}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* Center - Preview */}
        <main className="flex-1 flex flex-col min-w-0 relative">
          {/* Video preview */}
          <div className="flex-1 flex items-center justify-center relative p-4">
            <div className="aspect-video w-full max-w-4xl bg-surface-900 rounded-lg relative overflow-hidden">
              {/* Video element would go here */}
              <div className="absolute inset-0 flex items-center justify-center">
                <Video className="h-24 w-24 text-surface-600" aria-hidden="true" />
              </div>

              {/* Preview controls overlay */}
              <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 pointer-events-none">
                <div className="max-w-4xl mx-auto pointer-events-auto">
                  <div className="flex items-center gap-4 mb-2">
                    <button
                      onClick={() => setIsPlaying(!isPlaying)}
                      className="btn-ghost btn-lg text-white hover:bg-white/20"
                      aria-label={isPlaying ? 'Pause' : 'Play'}
                      aria-pressed={isPlaying}
                    >
                      {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
                    </button>
                    <button
                      onClick={() => setIsMuted(!isMuted)}
                      className="btn-ghost text-white hover:bg-white/20"
                      aria-label={isMuted ? 'Unmute' : 'Mute'}
                      aria-pressed={isMuted}
                    >
                      {isMuted ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
                    </button>
                    <div className="flex-1 h-1.5 bg-white/20 rounded-full relative cursor-pointer">
                      <div
                        className="h-full bg-brand-500 rounded-full transition-all"
                        style={{ width: `${(currentTime / duration) * 100}%` }}
                      />
                    </div>
                    <span className="text-body-xs text-white/80 font-mono w-20 text-right">
                      {formatTime(currentTime)} / {formatTime(duration)}
                    </span>
                    <button
                      className="btn-ghost text-white hover:bg-white/20"
                      aria-label="Fullscreen"
                    >
                      <Maximize className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Timeline */}
          <div className="h-64 border-t border-surface-800 bg-surface-900 relative">
            <div className="h-full flex">
              {/* Track headers */}
              <div className="w-32 border-r border-surface-800 flex flex-col p-2 bg-surface-900/50">
                {tracks.map((track) => (
                  <div key={track.id} className="flex-1 flex items-center gap-2 px-2 text-body-xs text-surface-400">
                    <div className={clsx('h-3 w-3 rounded', track.color)} />
                    <span>{track.name}</span>
                  </div>
                ))}
              </div>

              {/* Timeline tracks */}
              <div className="flex-1 relative overflow-x-auto">
                <div className="h-full min-w-[2000px] relative">
                  {/* Time ruler */}
                  <div className="h-8 border-b border-surface-800 bg-surface-900/50 flex items-end px-2">
                    {Array.from({ length: 31 }, (_, i) => (
                      <div
                        key={i}
                        className="w-[64px] flex flex-col items-center"
                        style={{ left: `${i * 64}px` }}
                      >
                        <div className="h-4 w-px bg-surface-600" />
                        <span className="text-[10px] text-surface-500">{i * 30}s</span>
                      </div>
                    ))}
                  </div>

                  {/* Track lanes */}
                  <div className="absolute top-8 left-0 right-0 bottom-0">
                    {tracks.map((track) => (
                      <div
                        key={track.id}
                        className="absolute left-0 right-0 h-20 border-b border-surface-800/50"
                        style={{ top: `${8 + tracks.indexOf(track) * 40}px` }}
                      >
                        {track.clips.map((clip) => (
                          <div
                            key={clip.id}
                            className="absolute h-16 rounded bg-brand-500/80 border border-brand-500 flex items-center justify-center px-2 text-white text-xs font-medium cursor-pointer hover:bg-brand-500 transition-colors"
                            style={{
                              left: `${(clip.start / duration) * 100}%`,
                              width: `${((clip.end - clip.start) / duration) * 100}%`,
                              top: '2px',
                            }}
                          >
                            {clip.name}
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>

                  {/* Playhead */}
                  <div
                    className="absolute top-8 bottom-0 w-px bg-brand-500 pointer-events-none"
                    style={{ left: `${(currentTime / duration) * 100}%` }}
                  >
                    <div className="absolute top-8 left-1/2 -translate-x-1/2 h-2 w-2 rounded-full bg-brand-500 border-2 border-surface-900" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Right sidebar - Inspector */}
        <aside className="hidden lg:flex lg:w-72 flex-col border-l border-surface-800 bg-surface-900">
          <div className="flex h-12 items-center justify-between border-b border-surface-800 px-4">
            <h2 className="text-body-sm font-medium text-white">Inspector</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            <div className="space-y-6">
              {/* Clip properties */}
              <section>
                <h3 className="text-body-sm font-medium text-surface-400 mb-4 uppercase tracking-wider">Clip Properties</h3>
                <div className="space-y-4">
                  <div>
                    <label className="label text-body-xs">Clip Name</label>
                    <input type="text" defaultValue="Highlight: AI in 2024" className="input bg-surface-800 border-surface-700 text-white" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="label text-body-xs">Start Time</label>
                      <input type="text" defaultValue="00:12:30" className="input bg-surface-800 border-surface-700 text-white" />
                    </div>
                    <div>
                      <label className="label text-body-xs">End Time</label>
                      <input type="text" defaultValue="00:15:45" className="input bg-surface-800 border-surface-700 text-white" />
                    </div>
                  </div>
                  <div>
                    <label className="label text-body-xs">Aspect Ratio</label>
                    <select className="input bg-surface-800 border-surface-700 text-white">
                      <option value="9:16">9:16 (Vertical)</option>
                      <option value="16:9">16:9 (Horizontal)</option>
                      <option value="1:1">1:1 (Square)</option>
                      <option value="4:5">4:5 (Portrait)</option>
                    </select>
                  </div>
                </div>
              </section>

              {/* Captions */}
              <section>
                <h3 className="text-body-sm font-medium text-surface-400 mb-4 uppercase tracking-wider">Captions</h3>
                <div className="space-y-3 max-h-60 overflow-y-auto">
                  {captions.map((caption) => (
                    <div key={caption.id} className="p-3 bg-surface-800 rounded-lg border border-surface-700">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-body-xs text-surface-500">{caption.time}</span>
                        <span className="text-body-xs text-brand-400">{caption.speaker}</span>
                      </div>
                      <p className="text-body-sm text-white">{caption.text}</p>
                    </div>
                  ))}
                </div>
              </section>

              {/* Effects */}
              <section>
                <h3 className="text-body-sm font-medium text-surface-400 mb-4 uppercase tracking-wider">Effects</h3>
                <div className="space-y-3">
                  {effects.map((effect) => (
                    <label key={effect.id} className="flex items-center gap-3 p-3 bg-surface-800 rounded-lg border border-surface-700 cursor-pointer hover:border-surface-600 transition-colors">
                      <input type="checkbox" defaultChecked={effect.enabled} className="h-4 w-4 rounded border-surface-600 text-brand-600 focus:ring-brand-500" />
                      <span className="text-body-sm text-white">{effect.name}</span>
                      {effect.description && <span className="text-body-xs text-surface-500 ml-auto">{effect.description}</span>}
                    </label>
                  ))}
                </div>
              </section>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

import { clsx } from 'clsx';

const clips = [
  { id: '1', name: 'Hook: AI Revolution', duration: '0:45', aspectRatio: '9:16' },
  { id: '2', name: 'Key Insight: LLMs', duration: '1:12', aspectRatio: '9:16' },
  { id: '3', name: 'Demo: Code Generation', duration: '0:58', aspectRatio: '16:9' },
  { id: '4', name: 'Future Predictions', duration: '1:03', aspectRatio: '9:16' },
  { id: '5', name: 'Q&A Highlights', duration: '0:41', aspectRatio: '1:1' },
  { id: '6', name: 'Call to Action', duration: '0:30', aspectRatio: '9:16' },
  { id: '7', name: 'Bonus: Tips & Tricks', duration: '0:55', aspectRatio: '16:9' },
  { id: '8', name: 'Outro', duration: '0:28', aspectRatio: '9:16' },
];

const tracks = [
  { id: 'video', name: 'Video', color: 'bg-brand-500', clips: [
    { id: '1', name: 'Clip 1', start: 0, end: 45 },
    { id: '2', name: 'Clip 2', start: 75, end: 187 },
    { id: '3', name: 'Clip 3', start: 210, end: 268 },
  ]},
  { id: 'audio', name: 'Audio', color: 'bg-emerald-500', clips: [
    { id: 'a1', name: 'Full Audio', start: 0, end: 1800 },
  ]},
  { id: 'captions', name: 'Captions', color: 'bg-amber-500', clips: [
    { id: 'c1', name: 'Caption 1', start: 10, end: 30 },
    { id: 'c2', name: 'Caption 2', start: 35, end: 55 },
  ]},
  { id: 'broll', name: 'B-Roll', color: 'bg-violet-500', clips: [
    { id: 'b1', name: 'B-Roll 1', start: 50, end: 80 },
  ]},
];

const captions = [
  { id: '1', time: '00:12:30', speaker: 'Speaker 1', text: 'Welcome everyone to today\'s episode about AI in 2024.' },
  { id: '2', time: '00:12:35', speaker: 'Speaker 1', text: 'We\'re going to cover the latest developments in large language models.' },
  { id: '3', time: '00:12:42', speaker: 'Speaker 2', text: 'It\'s incredible how far we\'ve come in just the past year.' },
  { id: '4', time: '00:12:48', speaker: 'Speaker 1', text: 'Absolutely. Let me show you a quick demo of code generation.' },
];

const effects = [
  { id: '1', name: 'Auto Reframe', enabled: true, description: 'Automatically crop to aspect ratio' },
  { id: '2', name: 'Caption Animation', enabled: true, description: 'Word-by-word highlight' },
  { id: '3', name: 'Background Music', enabled: false, description: 'Add royalty-free music' },
  { id: '4', name: 'Noise Reduction', enabled: true, description: 'Clean up audio' },
  { id: '5', name: 'Color Grading', enabled: false, description: 'Apply cinematic look' },
];