import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export interface Project {
  id: string;
  name: string;
  description?: string;
  aspectRatio: '16:9' | '9:16' | '1:1' | '4:3' | '21:9';
  frameRate: number;
  resolution: '720p' | '1080p' | '4k';
  duration: number;
  thumbnail?: string;
  status: 'draft' | 'processing' | 'completed' | 'archived';
  ownerId: string;
  teamId?: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  clips: Clip[];
  media: Media[];
}

export interface Clip {
  id: string;
  projectId: string;
  mediaId: string;
  name?: string;
  startTime: number;
  endTime: number;
  duration: number;
  track: number;
  volume: number;
  opacity: number;
  effects: ClipEffect[];
  createdAt: string;
  updatedAt: string;
}

export interface ClipEffect {
  id: string;
  type: 'color' | 'transform' | 'audio' | 'transition';
  name: string;
  params: Record<string, unknown>;
  enabled: boolean;
  order: number;
}

export interface Media {
  id: string;
  projectId?: string;
  filename: string;
  originalName: string;
  mimeType: string;
  size: number;
  duration?: number;
  width?: number;
  height?: number;
  thumbnail?: string;
  url: string;
  status: 'uploading' | 'processing' | 'ready' | 'error';
  metadata: MediaMetadata;
  createdAt: string;
}

export interface MediaMetadata {
  format?: string;
  codec?: string;
  bitrate?: number;
  sampleRate?: number;
  channels?: number;
  fps?: number;
  duration?: number;
}

export interface TranscriptSegment {
  id: string;
  mediaId: string;
  startTime: number;
  endTime: number;
  text: string;
  confidence: number;
  speaker?: string;
  words?: TranscriptWord[];
}

export interface TranscriptWord {
  word: string;
  startTime: number;
  endTime: number;
  confidence: number;
}

export interface TimelineState {
  zoom: number;
  playhead: number;
  duration: number;
  isPlaying: boolean;
  loopEnabled: boolean;
  snapEnabled: boolean;
  selectedClips: string[];
  hoveredClip: string | null;
}

interface ProjectState {
  // Projects
  projects: Project[];
  currentProject: Project | null;
  isLoadingProjects: boolean;
  projectsError: string | null;

  // Current project details
  clips: Clip[];
  media: Media[];
  transcripts: TranscriptSegment[];
  timeline: TimelineState;

  // UI state
  sidebarOpen: boolean;
  inspectorOpen: boolean;
  transcriptOpen: boolean;
  viewMode: 'timeline' | 'script' | 'scene';

  // Actions - Projects
  setProjects: (projects: Project[]) => void;
  addProject: (project: Project) => void;
  updateProject: (id: string, updates: Partial<Project>) => void;
  removeProject: (id: string) => void;
  setCurrentProject: (project: Project | null) => void;
  setProjectsLoading: (loading: boolean) => void;
  setProjectsError: (error: string | null) => void;

  // Actions - Clips
  setClips: (clips: Clip[]) => void;
  addClip: (clip: Clip) => void;
  updateClip: (id: string, updates: Partial<Clip>) => void;
  removeClip: (id: string) => void;
  reorderClips: (clips: Clip[]) => void;

  // Actions - Media
  setMedia: (media: Media[]) => void;
  addMedia: (media: Media) => void;
  updateMedia: (id: string, updates: Partial<Media>) => void;
  removeMedia: (id: string) => void;

  // Actions - Transcripts
  setTranscripts: (transcripts: TranscriptSegment[]) => void;
  updateTranscript: (id: string, updates: Partial<TranscriptSegment>) => void;

  // Actions - Timeline
  setTimeline: (timeline: Partial<TimelineState>) => void;
  setPlayhead: (time: number) => void;
  setZoom: (zoom: number) => void;
  setPlaying: (playing: boolean) => void;
  toggleLoop: () => void;
  toggleSnap: () => void;
  selectClip: (id: string, multi?: boolean) => void;
  clearSelection: () => void;
  hoverClip: (id: string | null) => void;

  // Actions - UI
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  toggleInspector: () => void;
  setInspectorOpen: (open: boolean) => void;
  toggleTranscript: () => void;
  setTranscriptOpen: (open: boolean) => void;
  setViewMode: (mode: 'timeline' | 'script' | 'scene') => void;

  // Reset
  resetProject: () => void;
}

const defaultTimeline: TimelineState = {
  zoom: 1,
  playhead: 0,
  duration: 0,
  isPlaying: false,
  loopEnabled: false,
  snapEnabled: true,
  selectedClips: [],
  hoveredClip: null,
};

export const useProjectStore = create<ProjectState>()(
  persist(
    (set, get) => ({
      projects: [],
      currentProject: null,
      isLoadingProjects: false,
      projectsError: null,

      clips: [],
      media: [],
      transcripts: [],
      timeline: defaultTimeline,

      sidebarOpen: true,
      inspectorOpen: true,
      transcriptOpen: false,
      viewMode: 'timeline',

      // Projects
      setProjects: (projects) => set({ projects }),

      addProject: (project) =>
        set((state) => ({ projects: [project, ...state.projects] })),

      updateProject: (id, updates) =>
        set((state) => ({
          projects: state.projects.map((p) =>
            p.id === id ? { ...p, ...updates, updatedAt: new Date().toISOString() } : p
          ),
          currentProject:
            state.currentProject?.id === id
              ? { ...state.currentProject, ...updates, updatedAt: new Date().toISOString() }
              : state.currentProject,
        })),

      removeProject: (id) =>
        set((state) => ({
          projects: state.projects.filter((p) => p.id !== id),
          currentProject: state.currentProject?.id === id ? null : state.currentProject,
        })),

      setCurrentProject: (project) =>
        set({
          currentProject: project,
          clips: project?.clips || [],
          media: project?.media || [],
          timeline: { ...defaultTimeline, duration: project?.duration || 0 },
        }),

      setProjectsLoading: (isLoadingProjects) => set({ isLoadingProjects }),

      setProjectsError: (projectsError) => set({ projectsError }),

      // Clips
      setClips: (clips) => set({ clips }),

      addClip: (clip) =>
        set((state) => ({
          clips: [...state.clips, clip],
          currentProject: state.currentProject
            ? { ...state.currentProject, clips: [...state.currentProject.clips, clip] }
            : null,
        })),

      updateClip: (id, updates) =>
        set((state) => ({
          clips: state.clips.map((c) =>
            c.id === id ? { ...c, ...updates, updatedAt: new Date().toISOString() } : c
          ),
          currentProject: state.currentProject
            ? {
                ...state.currentProject,
                clips: state.currentProject.clips.map((c) =>
                  c.id === id ? { ...c, ...updates, updatedAt: new Date().toISOString() } : c
                ),
              }
            : null,
        })),

      removeClip: (id) =>
        set((state) => ({
          clips: state.clips.filter((c) => c.id !== id),
          timeline: {
            ...state.timeline,
            selectedClips: state.timeline.selectedClips.filter((cid) => cid !== id),
          },
          currentProject: state.currentProject
            ? {
                ...state.currentProject,
                clips: state.currentProject.clips.filter((c) => c.id !== id),
              }
            : null,
        })),

      reorderClips: (clips) => set({ clips }),

      // Media
      setMedia: (media) => set({ media }),

      addMedia: (mediaItem) =>
        set((state) => ({
          media: [...state.media, mediaItem],
          currentProject: state.currentProject
            ? { ...state.currentProject, media: [...state.currentProject.media, mediaItem] }
            : null,
        })),

      updateMedia: (id, updates) =>
        set((state) => ({
          media: state.media.map((m) =>
            m.id === id ? { ...m, ...updates, updatedAt: new Date().toISOString() } : m
          ),
          currentProject: state.currentProject
            ? {
                ...state.currentProject,
                media: state.currentProject.media.map((m) =>
                  m.id === id ? { ...m, ...updates, updatedAt: new Date().toISOString() } : m
                ),
              }
            : null,
        })),

      removeMedia: (id) =>
        set((state) => ({
          media: state.media.filter((m) => m.id !== id),
          currentProject: state.currentProject
            ? {
                ...state.currentProject,
                media: state.currentProject.media.filter((m) => m.id !== id),
              }
            : null,
        })),

      // Transcripts
      setTranscripts: (transcripts) => set({ transcripts }),

      updateTranscript: (id, updates) =>
        set((state) => ({
          transcripts: state.transcripts.map((t) =>
            t.id === id ? { ...t, ...updates } : t
          ),
        })),

      // Timeline
      setTimeline: (timeline) =>
        set((state) => ({ timeline: { ...state.timeline, ...timeline } })),

      setPlayhead: (playhead) =>
        set((state) => ({ timeline: { ...state.timeline, playhead } })),

      setZoom: (zoom) =>
        set((state) => ({ timeline: { ...state.timeline, zoom: Math.max(0.1, Math.min(100, zoom)) } })),

      setPlaying: (isPlaying) =>
        set((state) => ({ timeline: { ...state.timeline, isPlaying } })),

      toggleLoop: () =>
        set((state) => ({
          timeline: { ...state.timeline, loopEnabled: !state.timeline.loopEnabled },
        })),

      toggleSnap: () =>
        set((state) => ({
          timeline: { ...state.timeline, snapEnabled: !state.timeline.snapEnabled },
        })),

      selectClip: (id, multi = false) =>
        set((state) => ({
          timeline: {
            ...state.timeline,
            selectedClips: multi
              ? state.timeline.selectedClips.includes(id)
                ? state.timeline.selectedClips.filter((cid) => cid !== id)
                : [...state.timeline.selectedClips, id]
              : [id],
          },
        })),

      clearSelection: () =>
        set((state) => ({
          timeline: { ...state.timeline, selectedClips: [] },
        })),

      hoverClip: (hoveredClip) =>
        set((state) => ({
          timeline: { ...state.timeline, hoveredClip },
        })),

      // UI
      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen })),

      setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),

      toggleInspector: () =>
        set((state) => ({ inspectorOpen: !state.inspectorOpen })),

      setInspectorOpen: (inspectorOpen) => set({ inspectorOpen }),

      toggleTranscript: () =>
        set((state) => ({ transcriptOpen: !state.transcriptOpen })),

      setTranscriptOpen: (transcriptOpen) => set({ transcriptOpen }),

      setViewMode: (viewMode) => set({ viewMode }),

      // Reset
      resetProject: () =>
        set({
          currentProject: null,
          clips: [],
          media: [],
          transcripts: [],
          timeline: defaultTimeline,
          sidebarOpen: true,
          inspectorOpen: true,
          transcriptOpen: false,
          viewMode: 'timeline',
        }),
    }),
    {
      name: 'clipyantra-project',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        projects: state.projects,
        sidebarOpen: state.sidebarOpen,
        inspectorOpen: state.inspectorOpen,
        transcriptOpen: state.transcriptOpen,
        viewMode: state.viewMode,
        timeline: {
          zoom: state.timeline.zoom,
          loopEnabled: state.timeline.loopEnabled,
          snapEnabled: state.timeline.snapEnabled,
        },
      }),
    }
  )
);