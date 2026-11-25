import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: string;
  teamId?: string;
  preferences: UserPreferences;
  createdAt: string;
  updatedAt: string;
}

interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  density: 'comfortable' | 'compact';
  animations: boolean;
  reducedMotion: boolean;
  language: string;
  dateFormat: string;
  timeFormat: string;
  notifications: NotificationPreferences;
}

interface NotificationPreferences {
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

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  setUser: (user: User | null) => void;
  setTokens: (accessToken: string, refreshToken: string) => void;
  clearAuth: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
  updateNotificationPreferences: (preferences: Partial<NotificationPreferences>) => void;
}

const defaultPreferences: UserPreferences = {
  theme: 'system',
  density: 'comfortable',
  animations: true,
  reducedMotion: false,
  language: 'en',
  dateFormat: 'MM/DD/YYYY',
  timeFormat: '12h',
  notifications: {
    email: {
      projectUpdates: true,
      comments: true,
      mentions: true,
      exports: true,
      marketing: false,
    },
    push: {
      projectUpdates: true,
      comments: true,
      mentions: true,
      exports: true,
    },
    inApp: {
      projectUpdates: true,
      comments: true,
      mentions: true,
      exports: true,
    },
  },
};

export const useUserStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      setUser: (user) =>
        set({
          user,
          isAuthenticated: !!user,
        }),

      setTokens: (accessToken, refreshToken) =>
        set({
          accessToken,
          refreshToken,
          isAuthenticated: true,
        }),

      clearAuth: () =>
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
          error: null,
        }),

      setLoading: (isLoading) => set({ isLoading }),

      setError: (error) => set({ error }),

      updatePreferences: (preferences) =>
        set((state) => ({
          user: state.user
            ? { ...state.user, preferences: { ...state.user.preferences, ...preferences } }
            : null,
        })),

      updateNotificationPreferences: (preferences) =>
        set((state) => ({
          user: state.user
            ? {
                ...state.user,
                preferences: {
                  ...state.user.preferences,
                  notifications: {
                    ...state.user.preferences.notifications,
                    ...preferences,
                  },
                },
              }
            : null,
        })),
    }),
    {
      name: 'clipyantra-auth',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// Selectors
export const getAccessToken = () => useUserStore.getState().accessToken;
export const getRefreshToken = () => useUserStore.getState().refreshToken;
export const getUser = () => useUserStore.getState().user;
export const isAuthenticated = () => useUserStore.getState().isAuthenticated;

export const setAccessToken = (token: string) => {
  useUserStore.getState().setTokens(token, useUserStore.getState().refreshToken || '');
};

export const clearTokens = () => {
  useUserStore.getState().clearAuth();
};