import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { ApiStatus } from './ApiStatus';

describe('ApiStatus', () => {
  beforeEach(() => vi.restoreAllMocks());

  it('shows a loading state first', () => {
    vi.stubGlobal('fetch', vi.fn(() => new Promise(() => {})));
    render(<ApiStatus />);
    expect(screen.getByRole('status')).toHaveTextContent('Checking API');
  });

  it('reports success when the API responds', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'ok' }) })),
    );
    render(<ApiStatus />);
    expect(await screen.findByText('API connected')).toBeInTheDocument();
  });

  it('shows an error state when the API is down', async () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.reject(new Error('network'))));
    render(<ApiStatus />);
    expect(await screen.findByRole('alert')).toHaveTextContent('API unreachable');
  });
});
