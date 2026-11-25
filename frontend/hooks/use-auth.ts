'use client';

import { useEffect, useCallback } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useUserStore, getAccessToken, setAccessToken, clearTokens } from '@/store/user-store';
import { api, endpoints } from '@/lib/api';

interface UseAuthOptions {
  required?: boolean;
  redirectTo?: string;
}

interface UseAuthReturn {
  user: ReturnType<typeof useUserStore>['user'];
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>;
  register: (data: { name: string; email: string; password: string; confirmPassword: string }) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  updateProfile: (data: Partial<ReturnType<typeof useUserStore>['user']>) => Promise<void>;
  changePassword: (currentPassword: string, newPassword: string) => Promise<void>;
}

export function useAuth(options: UseAuthOptions = {}): UseAuthReturn {
  const { required = false, redirectTo = '/login' } = options;
  const router = useRouter();
  const pathname = usePathname();

  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    setUser,
    setTokens,
    clearAuth,
    setLoading,
    setError,
  } = useUserStore();

  // Check auth on mount and when path changes
  useEffect(() => {
    const checkAuth = async () => {
      const token = getAccessToken();
      if (!token) {
        if (required) {
          router.push(`${redirectTo}?redirect=${encodeURIComponent(pathname)}`);
        }
        return;
      }

      setLoading(true);
      try {
        const userData = await api.get<{ user: typeof user }>(endpoints.auth.me);
        setUser(userData.user);
      } catch (err) {
        // Token might be expired, try to refresh
        try {
          const refreshToken = useUserStore.getState().refreshToken;
          if (refreshToken) {
            const response = await api.post<{ access_token: string }>(endpoints.auth.refresh, {
              refresh_token: refreshToken,
            });
            setAccessToken(response.access_token);
            const userData = await api.get<{ user: typeof user }>(endpoints.auth.me);
            setUser(userData.user);
          } else {
            throw err;
          }
        } catch {
          clearTokens();
          clearAuth();
          if (required) {
            router.push(`${redirectTo}?redirect=${encodeURIComponent(pathname)}`);
          }
        }
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [pathname, required, redirectTo, router, setUser, setTokens, setLoading, clearAuth, clearTokens]);

  const login = useCallback(async (email: string, password: string, rememberMe = false) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post<{ user: typeof user; access_token: string; refresh_token: string; expires_in: number }>(
        endpoints.auth.login,
        { email, password, remember_me: rememberMe }
      );
      setTokens(response.access_token, response.refresh_token);
      setUser(response.user);
      router.push('/dashboard');
      router.refresh();
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Login failed';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError, setTokens, setUser, router]);

  const register = useCallback(async (data: { name: string; email: string; password: string; confirmPassword: string }) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post<{ user: typeof user; access_token: string; refresh_token: string; expires_in: number }>(
        endpoints.auth.register,
        data
      );
      setTokens(response.access_token, response.refresh_token);
      setUser(response.user);
      router.push('/dashboard');
      router.refresh();
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Registration failed';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError, setTokens, setUser, router]);

  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await api.post(endpoints.auth.logout);
    } catch {
      // Ignore logout API errors
    } finally {
      clearTokens();
      clearAuth();
      router.push('/login');
      router.refresh();
      setLoading(false);
    }
  }, [setLoading, clearTokens, clearAuth, router]);

  const refreshUser = useCallback(async () => {
    try {
      const response = await api.get<{ user: typeof user }>(endpoints.auth.me);
      setUser(response.user);
    } catch (err) {
      console.error('Failed to refresh user:', err);
    }
  }, [setUser]);

  const updateProfile = useCallback(async (data: Partial<typeof user>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.put<{ user: typeof user }>(endpoints.users.profile, data);
      setUser(response.user);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to update profile';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError, setUser]);

  const changePassword = useCallback(async (currentPassword: string, newPassword: string) => {
    setLoading(true);
    setError(null);
    try {
      await api.post(endpoints.users.profile, {
        current_password: currentPassword,
        new_password: newPassword,
      });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to change password';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError]);

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    refreshUser,
    updateProfile,
    changePassword,
  };
}

// Hook for protecting routes - use in layout or page components
export function useRequireAuth(redirectTo = '/login') {
  const { isAuthenticated, isLoading, user } = useAuth({ required: true, redirectTo });

  // This will redirect automatically via the useAuth hook
  return { isAuthenticated, isLoading, user };
}

// Hook for guest-only routes (login, register pages)
export function useGuestOnly(redirectTo = '/dashboard') {
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      window.location.href = redirectTo;
    }
  }, [isAuthenticated, isLoading, redirectTo]);

  return { isAuthenticated, isLoading };
}