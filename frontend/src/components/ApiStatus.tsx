import { useEffect, useState } from 'react';
import { getHealth } from '../api/client';

type State = 'loading' | 'ok' | 'error';

/** EPIC 0's walking skeleton: proves React -> FastAPI -> Postgres round-trips
 *  in the deployed environment. Also the first place the three UI states that
 *  every screen must have (loading / empty-or-ok / error) are established. */
export function ApiStatus() {
  const [state, setState] = useState<State>('loading');

  useEffect(() => {
    let cancelled = false;
    getHealth()
      .then(() => !cancelled && setState('ok'))
      .catch(() => !cancelled && setState('error'));
    return () => {
      cancelled = true;
    };
  }, []);

  if (state === 'loading') return <p role="status">Checking API…</p>;
  if (state === 'error') return <p role="alert">API unreachable</p>;
  return <p role="status">API connected</p>;
}
