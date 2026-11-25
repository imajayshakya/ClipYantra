// Editor-specific types for the Clip Studio

export interface TimelineTrack {
  id: string;
  name: string;
  type: 'video' | 'audio' | 'text' | 'effect';
  height: number;
  locked: boolean;
  muted: boolean;
  solo: boolean;
  clips: TimelineClip[];
  color: string;
}

export interface TimelineClip {
  id: string;
  trackId: string;
  mediaId: string;
  name: string;
  startTime: number;
  endTime: number;
  duration: number;
  sourceStartTime: number;
  sourceEndTime: number;
  volume: number;
  opacity: number;
  effects: ClipEffect[];
  transform: ClipTransform;
  thumbnail?: string;
  waveform?: number[];
  color: string;
  locked: boolean;
}

export interface ClipEffect {
  id: string;
  type: EffectType;
  name: string;
  category: 'color' | 'transform' | 'audio' | 'transition' | 'text' | 'stylize';
  params: Record<string, EffectParam>;
  enabled: boolean;
  order: number;
  keyframes: EffectKeyframe[];
}

export type EffectType =
  // Color
  | 'brightness'
  | 'contrast'
  | 'saturation'
  | 'hue'
  | 'temperature'
  | 'tint'
  | 'exposure'
  | 'highlights'
  | 'shadows'
  | 'whites'
  | 'blacks'
  | 'vibrance'
  | 'colorWheels'
  | 'lut'
  // Transform
  | 'position'
  | 'scale'
  | 'rotation'
  | 'anchorPoint'
  | 'opacity'
  | 'crop'
  | 'cornerPin'
  // Audio
  | 'volume'
  | 'pan'
  | 'equalizer'
  | 'compressor'
  | 'noiseReduction'
  | 'pitchShift'
  // Transition
  | 'crossDissolve'
  | 'dipToBlack'
  | 'dipToWhite'
  | 'slide'
  | 'push'
  | 'wipe'
  | 'zoom'
  // Text
  | 'text'
  | 'lowerThird'
  | 'caption'
  | 'subtitle'
  // Stylize
  | 'blur'
  | 'sharpen'
  | 'vignette'
  | 'filmGrain'
  | 'glow'
  | 'lensFlare';

export interface EffectParam {
  value: number | string | boolean | ColorValue | PointValue;
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
  options?: string[];
}

export interface ColorValue {
  r: number;
  g: number;
  b: number;
  a?: number;
}

export interface PointValue {
  x: number;
  y: number;
}

export interface EffectKeyframe {
  time: number;
  value: number | string | boolean | ColorValue | PointValue;
  easing?: EasingType;
}

export type EasingType =
  | 'linear'
  | 'easeIn'
  | 'easeOut'
  | 'easeInOut'
  | 'easeInSine'
  | 'easeOutSine'
  | 'easeInOutSine'
  | 'easeInQuad'
  | 'easeOutQuad'
  | 'easeInOutQuad'
  | 'easeInCubic'
  | 'easeOutCubic'
  | 'easeInOutCubic'
  | 'easeInQuart'
  | 'easeOutQuart'
  | 'easeInOutQuart'
  | 'easeInQuint'
  | 'easeOutQuint'
  | 'easeInOutQuint'
  | 'easeInExpo'
  | 'easeOutExpo'
  | 'easeInOutExpo'
  | 'easeInCirc'
  | 'easeOutCirc'
  | 'easeInOutCirc'
  | 'easeInBack'
  | 'easeOutBack'
  | 'easeInOutBack'
  | 'easeInElastic'
  | 'easeOutElastic'
  | 'easeInOutElastic'
  | 'easeInBounce'
  | 'easeOutBounce'
  | 'easeInOutBounce';

export interface ClipTransform {
  position: { x: number; y: number };
  scale: { x: number; y: number };
  rotation: number;
  anchorPoint: { x: number; y: number };
  opacity: number;
  crop: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };
  cornerPin?: {
    topLeft: { x: number; y: number };
    topRight: { x: number; y: number };
    bottomLeft: { x: number; y: number };
    bottomRight: { x: number; y: number };
  };
}

// Preview types
export interface PreviewState {
  currentTime: number;
  duration: number;
  isPlaying: boolean;
  playbackRate: number;
  volume: number;
  muted: boolean;
  quality: 'auto' | '4k' | '1080p' | '720p' | '480p' | '360p';
  showSafeZones: boolean;
  showGuides: boolean;
  showTimecode: boolean;
  loopEnabled: boolean;
  fullscreen: boolean;
}

export interface SafeZone {
  type: 'title' | 'action';
  top: number;
  left: number;
  width: number;
  height: number;
}

// Transcript types
export interface TranscriptEditorState {
  segments: TranscriptSegment[];
  activeSegmentId: string | null;
  searchQuery: string;
  filterSpeaker: string | null;
  showTimestamps: boolean;
  showConfidence: boolean;
  autoScroll: boolean;
  editMode: boolean;
}

export interface TranscriptSegment {
  id: string;
  mediaId: string;
  startTime: number;
  endTime: number;
  text: string;
  originalText: string;
  confidence: number;
  speaker?: string;
  speakerId?: string;
  words?: TranscriptWord[];
  isEdited: boolean;
  editedAt?: string;
  editedBy?: string;
}

export interface TranscriptWord {
  id: string;
  word: string;
  startTime: number;
  endTime: number;
  confidence: number;
}

// Inspector types
export interface InspectorTab {
  id: 'clip' | 'effects' | 'transform' | 'audio' | 'color' | 'captions';
  label: string;
  icon: string;
  disabled?: boolean;
}

export interface ClipProperties {
  id: string;
  name: string;
  mediaId: string;
  mediaName: string;
  duration: number;
  startTime: number;
  endTime: number;
  track: number;
  fileInfo: {
    format: string;
    codec: string;
    resolution: string;
    frameRate: number;
    bitrate: number;
    audioChannels: number;
    audioSampleRate: number;
  };
}

export interface EffectStack {
  effects: ClipEffect[];
  selectedEffectId: string | null;
  searchQuery: string;
  categories: EffectCategory[];
}

export interface EffectCategory {
  id: string;
  name: string;
  effects: EffectType[];
  expanded: boolean;
}

// Keyboard shortcuts
export interface KeyboardShortcut {
  id: string;
  keys: string[];
  action: string;
  description: string;
  category: 'global' | 'timeline' | 'preview' | 'transcript' | 'inspector';
  context?: string;
  macKeys?: string[];
}

export const KEYBOARD_SHORTCUTS: KeyboardShortcut[] = [
  // Global
  { id: 'undo', keys: ['Control', 'z'], action: 'undo', description: 'Undo', category: 'global', macKeys: ['Meta', 'z'] },
  { id: 'redo', keys: ['Control', 'Shift', 'z'], action: 'redo', description: 'Redo', category: 'global', macKeys: ['Meta', 'Shift', 'z'] },
  { id: 'save', keys: ['Control', 's'], action: 'save', description: 'Save project', category: 'global', macKeys: ['Meta', 's'] },
  { id: 'copy', keys: ['Control', 'c'], action: 'copy', description: 'Copy', category: 'global', macKeys: ['Meta', 'c'] },
  { id: 'paste', keys: ['Control', 'v'], action: 'paste', description: 'Paste', category: 'global', macKeys: ['Meta', 'v'] },
  { id: 'cut', keys: ['Control', 'x'], action: 'cut', description: 'Cut', category: 'global', macKeys: ['Meta', 'x'] },
  { id: 'duplicate', keys: ['Control', 'd'], action: 'duplicate', description: 'Duplicate', category: 'global', macKeys: ['Meta', 'd'] },
  { id: 'delete', keys: ['Delete'], action: 'delete', description: 'Delete', category: 'global' },
  { id: 'selectAll', keys: ['Control', 'a'], action: 'selectAll', description: 'Select all', category: 'global', macKeys: ['Meta', 'a'] },
  { id: 'find', keys: ['Control', 'f'], action: 'find', description: 'Find', category: 'global', macKeys: ['Meta', 'f'] },
  { id: 'preferences', keys: ['Control', ','], action: 'preferences', description: 'Preferences', category: 'global', macKeys: ['Meta', ','] },

  // Timeline
  { id: 'playPause', keys: ['Space'], action: 'playPause', description: 'Play/Pause', category: 'timeline' },
  { id: 'stop', keys: ['KeyK'], action: 'stop', description: 'Stop', category: 'timeline' },
  { id: 'stepForward', keys: ['ArrowRight'], action: 'stepForward', description: 'Step forward 1 frame', category: 'timeline' },
  { id: 'stepBackward', keys: ['ArrowLeft'], action: 'stepBackward', description: 'Step backward 1 frame', category: 'timeline' },
  { id: 'jumpForward', keys: ['Shift', 'ArrowRight'], action: 'jumpForward', description: 'Jump forward 1 second', category: 'timeline' },
  { id: 'jumpBackward', keys: ['Shift', 'ArrowLeft'], action: 'jumpBackward', description: 'Jump backward 1 second', category: 'timeline' },
  { id: 'gotoStart', keys: ['Home'], action: 'gotoStart', description: 'Go to start', category: 'timeline' },
  { id: 'gotoEnd', keys: ['End'], action: 'gotoEnd', description: 'Go to end', category: 'timeline' },
  { id: 'zoomIn', keys: ['Equal'], action: 'zoomIn', description: 'Zoom in', category: 'timeline', macKeys: ['Meta', '='] },
  { id: 'zoomOut', keys: ['Minus'], action: 'zoomOut', description: 'Zoom out', category: 'timeline', macKeys: ['Meta', '-'] },
  { id: 'zoomToFit', keys: ['Shift', 'Equal'], action: 'zoomToFit', description: 'Zoom to fit', category: 'timeline', macKeys: ['Shift', 'Meta', '='] },
  { id: 'addVideoTrack', keys: ['Control', 'Alt', 'v'], action: 'addVideoTrack', description: 'Add video track', category: 'timeline', macKeys: ['Meta', 'Alt', 'v'] },
  { id: 'addAudioTrack', keys: ['Control', 'Alt', 'a'], action: 'addAudioTrack', description: 'Add audio track', category: 'timeline', macKeys: ['Meta', 'Alt', 'a'] },
  { id: 'toggleSnap', keys: ['KeyS'], action: 'toggleSnap', description: 'Toggle snap', category: 'timeline' },
  { id: 'toggleLoop', keys: ['KeyL'], action: 'toggleLoop', description: 'Toggle loop', category: 'timeline' },
  { id: 'splitClip', keys: ['Control', 'KeyB'], action: 'splitClip', description: 'Split clip at playhead', category: 'timeline', macKeys: ['Meta', 'KeyB'] },
  { id: 'rippleDelete', keys: ['Shift', 'Delete'], action: 'rippleDelete', description: 'Ripple delete', category: 'timeline' },

  // Preview
  { id: 'toggleFullscreen', keys: ['KeyF'], action: 'toggleFullscreen', description: 'Toggle fullscreen', category: 'preview' },
  { id: 'toggleSafeZones', keys: ['Control', 'Shift', '\''], action: 'toggleSafeZones', description: 'Toggle safe zones', category: 'preview', macKeys: ['Meta', 'Shift', '\''] },
  { id: 'toggleGuides', keys: ['Control', ';'], action: 'toggleGuides', description: 'Toggle guides', category: 'preview', macKeys: ['Meta', ';'] },
  { id: 'toggleTimecode', keys: ['Control', 'Shift', 'KeyT'], action: 'toggleTimecode', description: 'Toggle timecode', category: 'preview', macKeys: ['Meta', 'Shift', 'KeyT'] },

  // Inspector
  { id: 'toggleInspector', keys: ['KeyI'], action: 'toggleInspector', description: 'Toggle inspector', category: 'inspector' },
  { id: 'focusClipTab', keys: ['Digit1'], action: 'focusClipTab', description: 'Focus clip properties', category: 'inspector' },
  { id: 'focusEffectsTab', keys: ['Digit2'], action: 'focusEffectsTab', description: 'Focus effects', category: 'inspector' },
  { id: 'focusTransformTab', keys: ['Digit3'], action: 'focusTransformTab', description: 'Focus transform', category: 'inspector' },
  { id: 'focusAudioTab', keys: ['Digit4'], action: 'focusAudioTab', description: 'Focus audio', category: 'inspector' },
  { id: 'focusColorTab', keys: ['Digit5'], action: 'focusColorTab', description: 'Focus color', category: 'inspector' },
  { id: 'focusCaptionsTab', keys: ['Digit6'], action: 'focusCaptionsTab', description: 'Focus captions', category: 'inspector' },

  // Transcript
  { id: 'toggleTranscript', keys: ['KeyT'], action: 'toggleTranscript', description: 'Toggle transcript', category: 'transcript' },
  { id: 'nextSegment', keys: ['Tab'], action: 'nextSegment', description: 'Next segment', category: 'transcript' },
  { id: 'prevSegment', keys: ['Shift', 'Tab'], action: 'prevSegment', description: 'Previous segment', category: 'transcript' },
  { id: 'playSegment', keys: ['Enter'], action: 'playSegment', description: 'Play segment', category: 'transcript' },
];

// Export/Share
export interface ShareSettings {
  enabled: boolean;
  url?: string;
  password?: string;
  expiresAt?: string;
  allowDownload: boolean;
  allowComments: boolean;
  watermark: boolean;
}

export interface CollaborationUser {
  id: string;
  name: string;
  color: string;
  cursor?: { x: number; y: number };
  selection?: string[];
  lastActive: string;
}

// Project templates
export interface ProjectTemplate {
  id: string;
  name: string;
  description: string;
  thumbnail: string;
  category: 'social' | 'youtube' | 'tiktok' | 'reels' | 'presentation' | 'podcast' | 'custom';
  aspectRatio: '16:9' | '9:16' | '1:1' | '4:3' | '21:9';
  frameRate: number;
  resolution: '720p' | '1080p' | '4k';
  duration: number;
  tracks: Omit<TimelineTrack, 'id' | 'clips'>[];
  effects: ClipEffect[];
  tags: string[];
  isDefault: boolean;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

// Version history
export interface ProjectVersion {
  id: string;
  projectId: string;
  name: string;
  description?: string;
  thumbnail?: string;
  authorId: string;
  authorName: string;
  changes: VersionChange[];
  snapshot: ProjectSnapshot;
  createdAt: string;
}

export interface VersionChange {
  type: 'clip_added' | 'clip_removed' | 'clip_updated' | 'track_added' | 'track_removed' | 'effect_added' | 'effect_removed' | 'effect_updated' | 'setting_changed';
  entityId: string;
  entityType: 'clip' | 'track' | 'effect' | 'project';
  previousValue?: unknown;
  newValue?: unknown;
}

export interface ProjectSnapshot {
  tracks: TimelineTrack[];
  settings: ProjectSettings;
  duration: number;
}