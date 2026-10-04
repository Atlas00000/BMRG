import { useEffect, useState } from 'react';

type LoadState<T> =
  | { status: 'loading' }
  | { status: 'ok'; data: T }
  | { status: 'error'; message: string; path: string };

export function useAsync<T>(loader: () => Promise<T>, deps: unknown[] = []): LoadState<T> {
  const [state, setState] = useState<LoadState<T>>({ status: 'loading' });

  useEffect(() => {
    let cancelled = false;
    setState({ status: 'loading' });
    loader()
      .then((data) => {
        if (!cancelled) setState({ status: 'ok', data });
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        const message = err instanceof Error ? err.message : String(err);
        const path =
          err && typeof err === 'object' && 'path' in err
            ? String((err as { path: string }).path)
            : 'unknown';
        setState({ status: 'error', message, path });
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}
