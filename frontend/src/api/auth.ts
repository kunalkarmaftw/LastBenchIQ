/** Auth API calls and token storage. */

import { apiFetch, ApiError } from './client';

export interface User {
  id: string;
  enrollment_number: string;
  email: string;
  name: string;
  college: string | null;
  branch: string | null;
  graduation_year: number | null;
  career_goal: 'mba' | 'job' | 'undecided';
  target_role: string | null;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface SignupInput {
  enrollment_number: string;
  email: string;
  password: string;
  name: string;
  college?: string;
  branch?: string;
  graduation_year?: number;
}

const TOKEN_KEY = 'lbq_token';

/** localStorage throws in private windows and when site data is blocked.
 *  A failure here must never stop the page rendering. */
export const tokenStore = {
  get(): string | null {
    try { return localStorage.getItem(TOKEN_KEY); } catch { return null; }
  },
  set(token: string): void {
    try { localStorage.setItem(TOKEN_KEY, token); } catch { /* session-only */ }
  },
  clear(): void {
    try { localStorage.removeItem(TOKEN_KEY); } catch { /* nothing to do */ }
  },
};

export const signup = (input: SignupInput) =>
  apiFetch<AuthResponse>('/auth/register', { method: 'POST', body: JSON.stringify(input) });

export const login = (enrollment_number: string, password: string) =>
  apiFetch<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ enrollment_number, password }),
  });

export const fetchMe = () => apiFetch<User>('/auth/me');

/** The API nests its message under `detail` for auth errors. */
export function messageFor(err: unknown): string {
  if (err instanceof ApiError) {
    const d = err.detail as unknown;
    if (d && typeof d === 'object' && 'detail' in d) {
      const inner = (d as { detail?: unknown }).detail;
      if (typeof inner === 'string') return inner;
    }
    if (typeof d === 'string') return d;
    if (err.status === 422) return 'Please check the details you entered.';
    return err.message;
  }
  return 'Could not reach the server. Is the backend running?';
}
