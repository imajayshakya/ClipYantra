// Generated API types from OpenAPI specification
// This file should be auto-generated from the backend OpenAPI spec
// Run: npx openapi-typescript http://localhost:8000/openapi.json -o types/api.ts

export interface ApiResponse<T> {
  data: T;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
    totalPages?: number;
  };
  errors?: ApiError[];
}

export interface ApiError {
  code: string;
  message: string;
  field?: string;
  details?: Record<string, unknown>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface HealthCheckResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  environment: string;
  checks: Record<string, 'connected' | 'disconnected' | 'degraded'>;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface LoginResponse {
  user: User;
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  terms: boolean;
}

export interface RegisterResponse {
  user: User;
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface RefreshTokenRequest {
  refreshToken: string;
}

export interface RefreshTokenResponse {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  password: string;
  confirmPassword: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: 'user' | 'admin' | 'owner';
  teamId?: string;
  emailVerified: boolean;
  twoFactorEnabled: boolean;
  preferences: UserPreferences;
  createdAt: string;
  updatedAt: string;
  lastLoginAt?: string;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  density: 'comfortable' | 'compact';
  animations: boolean;
  reducedMotion: boolean;
  language: string;
  dateFormat: string;
  timeFormat: string;
  notifications: NotificationPreferences;
}

export interface NotificationPreferences {
  email: {
    projectUpdates: boolean;
    comments: boolean;
    mentions: boolean;
    exports: boolean;
    marketing: boolean;
  };
  push: {
    projectUpdates: boolean;
    comments: boolean;
    mentions: boolean;
    exports: boolean;
  };
  inApp: {
    projectUpdates: boolean;
    comments: boolean;
    mentions: boolean;
    exports: boolean;
  };
}

// Project types
export interface Project {
  id: string;
  name: string;
  description?: string;
  aspectRatio: '16:9' | '9:16' | '1:1' | '4:3' | '21:9';
  frameRate: 24 | 25 | 30 | 50 | 60;
  resolution: '720p' | '1080p' | '4k';
  duration: number;
  thumbnail?: string;
  status: 'draft' | 'processing' | 'completed' | 'archived';
  ownerId: string;
  teamId?: string;
  tags: string[];
  settings: ProjectSettings;
  createdAt: string;
  updatedAt: string;
}

export interface ProjectSettings {
  autoSave: boolean;
  autoSaveInterval: number;
  snapToGrid: boolean;
  showAudioWaveforms: boolean;
  showTimecode: boolean;
  defaultTransitionDuration: number;
  defaultClipDuration: number;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
  aspectRatio?: '16:9' | '9:16' | '1:1' | '4:3' | '21:9';
  frameRate?: 24 | 25 | 30 | 50 | 60;
  resolution?: '720p' | '1080p' | '4k';
  settings?: Partial<ProjectSettings>;
}

export interface UpdateProjectRequest extends Partial<CreateProjectRequest> {}

export interface ProjectListParams {
  page?: number;
  limit?: number;
  search?: string;
  status?: Project['status'][];
  sortBy?: 'createdAt' | 'updatedAt' | 'name' | 'duration';
  sortOrder?: 'asc' | 'desc';
  teamId?: string;
}

// Clip types
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
  transform: ClipTransform;
  createdAt: string;
  updatedAt: string;
}

export interface ClipEffect {
  id: string;
  type: 'color' | 'transform' | 'audio' | 'transition' | 'text' | 'blur' | 'sharpen';
  name: string;
  params: Record<string, unknown>;
  enabled: boolean;
  order: number;
}

export interface ClipTransform {
  position: { x: number; y: number };
  scale: { x: number; y: number };
  rotation: number;
  anchorPoint: { x: number; y: number };
  opacity: number;
}

export interface CreateClipRequest {
  projectId: string;
  mediaId: string;
  startTime: number;
  endTime: number;
  track?: number;
  name?: string;
}

export interface UpdateClipRequest {
  startTime?: number;
  endTime?: number;
  track?: number;
  name?: string;
  volume?: number;
  opacity?: number;
  effects?: ClipEffect[];
  transform?: Partial<ClipTransform>;
}

export interface ReorderClipsRequest {
  clips: { id: string; track: number; startTime: number }[];
}

// Media types
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
  proxyUrl?: string;
  status: 'uploading' | 'processing' | 'ready' | 'error';
  metadata: MediaMetadata;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface MediaMetadata {
  format?: string;
  codec?: string;
  bitrate?: number;
  sampleRate?: number;
  channels?: number;
  fps?: number;
  duration?: number;
  width?: number;
  height?: number;
  aspectRatio?: string;
  colorSpace?: string;
  hasAudio?: boolean;
  hasVideo?: boolean;
}

export interface UploadMediaRequest {
  file: File;
  projectId?: string;
  tags?: string[];
}

export interface UploadMediaResponse {
  media: Media;
  uploadUrl?: string;
}

// Transcript types
export interface Transcript {
  id: string;
  mediaId: string;
  language: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  segments: TranscriptSegment[];
  createdAt: string;
  updatedAt: string;
}

export interface TranscriptSegment {
  id: string;
  startTime: number;
  endTime: number;
  text: string;
  confidence: number;
  speaker?: string;
  words?: TranscriptWord[];
  isEdited: boolean;
}

export interface TranscriptWord {
  word: string;
  startTime: number;
  endTime: number;
  confidence: number;
}

export interface UpdateTranscriptRequest {
  segments: Partial<TranscriptSegment>[];
}

// Export types
export interface ExportSettings {
  format: 'mp4' | 'mov' | 'webm' | 'gif';
  resolution: '720p' | '1080p' | '4k';
  frameRate: 24 | 25 | 30 | 50 | 60;
  bitrate: number;
  codec: 'h264' | 'h265' | 'vp9' | 'av1';
  audioCodec: 'aac' | 'mp3' | 'opus';
  audioBitrate: number;
  includeCaptions: boolean;
  captionFormat?: 'srt' | 'vtt' | 'ass';
  watermark?: WatermarkSettings;
  colorSpace: 'rec709' | 'rec2020' | 'p3';
  hdr: boolean;
}

export interface WatermarkSettings {
  enabled: boolean;
  text?: string;
  imageUrl?: string;
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center';
  opacity: number;
  size: number;
}

export interface ExportJob {
  id: string;
  projectId: string;
  settings: ExportSettings;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;
  outputUrl?: string;
  error?: string;
  startedAt?: string;
  completedAt?: string;
  createdAt: string;
}

export interface CreateExportRequest {
  projectId: string;
  settings: ExportSettings;
}

// Team types
export interface Team {
  id: string;
  name: string;
  description?: string;
  avatar?: string;
  ownerId: string;
  plan: 'free' | 'pro' | 'business' | 'enterprise';
  memberCount: number;
  projectCount: number;
  storageUsed: number;
  storageLimit: number;
  settings: TeamSettings;
  createdAt: string;
  updatedAt: string;
}

export interface TeamSettings {
  defaultProjectVisibility: 'private' | 'team';
  allowGuestAccess: boolean;
  requireTwoFactor: boolean;
  allowedDomains?: string[];
}

export interface CreateTeamRequest {
  name: string;
  description?: string;
}

export interface UpdateTeamRequest extends Partial<CreateTeamRequest> {}

export interface TeamMember {
  id: string;
  teamId: string;
  userId: string;
  user: User;
  role: 'owner' | 'admin' | 'editor' | 'viewer';
  invitedBy: string;
  invitedAt: string;
  joinedAt?: string;
}

export interface InviteTeamMemberRequest {
  email: string;
  role: 'admin' | 'editor' | 'viewer';
}

export interface UpdateTeamMemberRequest {
  role: 'admin' | 'editor' | 'viewer';
}

// Billing types
export interface Plan {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  interval: 'month' | 'year';
  features: string[];
  limits: PlanLimits;
  popular: boolean;
}

export interface PlanLimits {
  projects: number;
  teamMembers: number;
  storage: number; // in GB
  exportMinutes: number;
  transcriptionMinutes: number;
  apiCalls: number;
}

export interface Subscription {
  id: string;
  teamId: string;
  planId: string;
  plan: Plan;
  status: 'active' | 'canceled' | 'past_due' | 'trialing' | 'incomplete';
  currentPeriodStart: string;
  currentPeriodEnd: string;
  cancelAtPeriodEnd: boolean;
  trialEnd?: string;
  paymentMethod?: PaymentMethod;
}

export interface PaymentMethod {
  id: string;
  type: 'card' | 'bank_account';
  brand?: string;
  last4?: string;
  expiryMonth?: number;
  expiryYear?: number;
}

export interface Invoice {
  id: string;
  subscriptionId: string;
  amount: number;
  currency: string;
  status: 'paid' | 'open' | 'void' | 'uncollectible';
  invoiceUrl: string;
  pdfUrl: string;
  periodStart: string;
  periodEnd: string;
  createdAt: string;
}

// Webhook types
export interface WebhookEvent {
  id: string;
  type: string;
  data: Record<string, unknown>;
  createdAt: string;
}

export interface WebhookSubscription {
  id: string;
  url: string;
  events: string[];
  secret: string;
  active: boolean;
  createdAt: string;
}

// Error codes
export const ERROR_CODES = {
  AUTH_INVALID_CREDENTIALS: 'AUTH_INVALID_CREDENTIALS',
  AUTH_TOKEN_EXPIRED: 'AUTH_TOKEN_EXPIRED',
  AUTH_TOKEN_INVALID: 'AUTH_TOKEN_INVALID',
  AUTH_UNAUTHORIZED: 'AUTH_UNAUTHORIZED',
  AUTH_FORBIDDEN: 'AUTH_FORBIDDEN',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  RESOURCE_NOT_FOUND: 'RESOURCE_NOT_FOUND',
  RESOURCE_CONFLICT: 'RESOURCE_CONFLICT',
  RATE_LIMIT_EXCEEDED: 'RATE_LIMIT_EXCEEDED',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  SERVICE_UNAVAILABLE: 'SERVICE_UNAVAILABLE',
  UPLOAD_FAILED: 'UPLOAD_FAILED',
  EXPORT_FAILED: 'EXPORT_FAILED',
  TRANSCRIPTION_FAILED: 'TRANSCRIPTION_FAILED',
} as const;

export type ErrorCode = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];