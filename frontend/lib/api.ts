import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios';
import { getAccessToken, setAccessToken, clearTokens } from '@/store/user-store';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = getAccessToken();
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = getAccessToken(); // In real app, get from secure storage
            if (refreshToken) {
              const response = await axios.post(`${API_URL}/auth/refresh`, {
                refresh_token: refreshToken,
              });
              const { access_token } = response.data;
              setAccessToken(access_token);
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${access_token}`;
              }
              return this.client(originalRequest);
            }
          } catch (refreshError) {
            clearTokens();
            if (typeof window !== 'undefined') {
              window.location.href = '/login';
            }
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Generic request methods
  async get<T>(url: string, config?: AxiosRequestConfig) {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async patch<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig) {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  // Upload with progress
  async upload<T>(
    url: string,
    formData: FormData,
    onProgress?: (progress: number) => void
  ) {
    const response = await this.client.post<T>(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    });
    return response.data;
  }

  // Health check
  async healthCheck() {
    return this.get<{ status: string; timestamp: string }>('/health');
  }
}

export const api = new ApiClient();

// API endpoint helpers
export const endpoints = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    logout: '/auth/logout',
    refresh: '/auth/refresh',
    me: '/auth/me',
    forgotPassword: '/auth/forgot-password',
    resetPassword: '/auth/reset-password',
  },
  projects: {
    list: '/projects',
    create: '/projects',
    get: (id: string) => `/projects/${id}`,
    update: (id: string) => `/projects/${id}`,
    delete: (id: string) => `/projects/${id}`,
    clips: (id: string) => `/projects/${id}/clips`,
    export: (id: string) => `/projects/${id}/export`,
  },
  clips: {
    list: '/clips',
    get: (id: string) => `/clips/${id}`,
    update: (id: string) => `/clips/${id}`,
    delete: (id: string) => `/clips/${id}`,
    download: (id: string) => `/clips/${id}/download`,
  },
  media: {
    upload: '/media/upload',
    get: (id: string) => `/media/${id}`,
    delete: (id: string) => `/media/${id}`,
  },
  transcripts: {
    get: (id: string) => `/transcripts/${id}`,
    update: (id: string) => `/transcripts/${id}`,
  },
  users: {
    profile: '/users/profile',
    update: '/users/profile',
    settings: '/users/settings',
    sessions: '/users/sessions',
  },
  teams: {
    list: '/teams',
    create: '/teams',
    get: (id: string) => `/teams/${id}`,
    update: (id: string) => `/teams/${id}`,
    members: (id: string) => `/teams/${id}/members`,
  },
  billing: {
    plans: '/billing/plans',
    subscription: '/billing/subscription',
    invoices: '/billing/invoices',
    checkout: '/billing/checkout',
  },
} as const;