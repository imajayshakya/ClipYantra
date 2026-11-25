import { z } from 'zod';

// Auth validations
export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  rememberMe: z.boolean().optional(),
});

export const registerSchema = z
  .object({
    name: z.string().min(2, 'Name must be at least 2 characters').max(100),
    email: z.string().email('Invalid email address'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
      .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
      .regex(/[0-9]/, 'Password must contain at least one number')
      .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character'),
    confirmPassword: z.string(),
    terms: z.boolean().refine((val) => val === true, 'You must accept the terms and conditions'),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

export const forgotPasswordSchema = z.object({
  email: z.string().email('Invalid email address'),
});

export const resetPasswordSchema = z
  .object({
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
      .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
      .regex(/[0-9]/, 'Password must contain at least one number')
      .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

// Project validations
export const projectCreateSchema = z.object({
  name: z.string().min(1, 'Project name is required').max(100),
  description: z.string().max(500).optional(),
  aspectRatio: z.enum(['16:9', '9:16', '1:1', '4:3', '21:9']).default('16:9'),
  frameRate: z.number().int().min(24).max(60).default(30),
  resolution: z.enum(['720p', '1080p', '4k']).default('1080p'),
});

export const projectUpdateSchema = projectCreateSchema.partial();

// Clip validations
export const clipCreateSchema = z.object({
  projectId: z.string().uuid('Invalid project ID'),
  mediaId: z.string().uuid('Invalid media ID'),
  startTime: z.number().min(0, 'Start time must be positive'),
  endTime: z.number().min(0, 'End time must be positive'),
  track: z.number().int().min(0).default(0),
  name: z.string().max(100).optional(),
});

export const clipUpdateSchema = z.object({
  startTime: z.number().min(0).optional(),
  endTime: z.number().min(0).optional(),
  track: z.number().int().min(0).optional(),
  name: z.string().max(100).optional(),
  volume: z.number().min(0).max(2).optional(),
  opacity: z.number().min(0).max(1).optional(),
});

// Media validations
export const mediaUploadSchema = z.object({
  file: z.instanceof(File, { message: 'File is required' }),
  projectId: z.string().uuid().optional(),
});

// Settings validations
export const profileUpdateSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(100),
  email: z.string().email('Invalid email address'),
  bio: z.string().max(500).optional(),
  timezone: z.string().optional(),
});

export const passwordUpdateSchema = z
  .object({
    currentPassword: z.string().min(1, 'Current password is required'),
    newPassword: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
      .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
      .regex(/[0-9]/, 'Password must contain at least one number')
      .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.newPassword === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

export const notificationSettingsSchema = z.object({
  email: z.object({
    projectUpdates: z.boolean(),
    comments: z.boolean(),
    mentions: z.boolean(),
    exports: z.boolean(),
    marketing: z.boolean(),
  }),
  push: z.object({
    projectUpdates: z.boolean(),
    comments: z.boolean(),
    mentions: z.boolean(),
    exports: z.boolean(),
  }),
  inApp: z.object({
    projectUpdates: z.boolean(),
    comments: z.boolean(),
    mentions: z.boolean(),
    exports: z.boolean(),
  }),
});

export const appearanceSettingsSchema = z.object({
  theme: z.enum(['light', 'dark', 'system']),
  density: z.enum(['comfortable', 'compact']),
  animations: z.boolean(),
  reducedMotion: z.boolean(),
});

export const languageSettingsSchema = z.object({
  language: z.string().min(2).max(5),
  dateFormat: z.enum(['MM/DD/YYYY', 'DD/MM/YYYY', 'YYYY-MM-DD']),
  timeFormat: z.enum(['12h', '24h']),
});

// Team validations
export const teamCreateSchema = z.object({
  name: z.string().min(1, 'Team name is required').max(100),
  description: z.string().max(500).optional(),
});

export const teamUpdateSchema = teamCreateSchema.partial();

export const teamInviteSchema = z.object({
  email: z.string().email('Invalid email address'),
  role: z.enum(['admin', 'editor', 'viewer']),
});

// Export validations
export const exportSettingsSchema = z.object({
  format: z.enum(['mp4', 'mov', 'webm']),
  resolution: z.enum(['720p', '1080p', '4k']),
  frameRate: z.number().int().min(24).max(60),
  bitrate: z.number().int().min(1000).max(50000),
  codec: z.enum(['h264', 'h265', 'vp9']),
  includeCaptions: z.boolean(),
  watermark: z.string().optional(),
});

// Type exports
export type LoginInput = z.infer<typeof loginSchema>;
export type RegisterInput = z.infer<typeof registerSchema>;
export type ForgotPasswordInput = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordInput = z.infer<typeof resetPasswordSchema>;
export type ProjectCreateInput = z.infer<typeof projectCreateSchema>;
export type ProjectUpdateInput = z.infer<typeof projectUpdateSchema>;
export type ClipCreateInput = z.infer<typeof clipCreateSchema>;
export type ClipUpdateInput = z.infer<typeof clipUpdateSchema>;
export type MediaUploadInput = z.infer<typeof mediaUploadSchema>;
export type ProfileUpdateInput = z.infer<typeof profileUpdateSchema>;
export type PasswordUpdateInput = z.infer<typeof passwordUpdateSchema>;
export type NotificationSettingsInput = z.infer<typeof notificationSettingsSchema>;
export type AppearanceSettingsInput = z.infer<typeof appearanceSettingsSchema>;
export type LanguageSettingsInput = z.infer<typeof languageSettingsSchema>;
export type TeamCreateInput = z.infer<typeof teamCreateSchema>;
export type TeamUpdateInput = z.infer<typeof teamUpdateSchema>;
export type TeamInviteInput = z.infer<typeof teamInviteSchema>;
export type ExportSettingsInput = z.infer<typeof exportSettingsSchema>;