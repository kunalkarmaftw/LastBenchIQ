/** Thin fetch wrapper. Every call goes through here so auth, errors and the
 *  base URL have exactly one definition. */

const BASE_URL = '/api/v1';

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly code?: string,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

function authHeaders(): Record<string, string> {
  // localStorage throws in some privacy modes — never let that break a render.
  try {
    const token = localStorage.getItem('lbq_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  } catch {
    return {};
  }
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...authHeaders(), ...init.headers },
  });

  if (!response.ok) {
    const body = (await response.json().catch(() => ({}))) as {
      detail?: string;
      code?: string;
    };
    throw new ApiError(body.detail ?? response.statusText, response.status, body.code);
  }
  return (await response.json()) as T;
}

export interface HealthResponse {
  status: string;
}

export const getHealth = () => apiFetch<HealthResponse>('/health');
