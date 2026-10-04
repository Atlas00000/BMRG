import { useEffect, useState } from 'react';
import type { BaselineDto, PinDto } from '../../api/adapters/artefacts';
import { ArtefactError, fetchBaseline, fetchPin } from './client';

type LoadState<T> =
  | { status: 'loading' }
  | { status: 'ok'; data: T }
  | { status: 'error'; message: string; path: string };

export function useBaseline(): LoadState<BaselineDto> {
  const [state, setState] = useState<LoadState<BaselineDto>>({ status: 'loading' });

  useEffect(() => {
    let cancelled = false;
    fetchBaseline()
      .then((data) => {
        if (!cancelled) setState({ status: 'ok', data });
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        if (err instanceof ArtefactError) {
          setState({ status: 'error', message: err.message, path: err.path });
        } else {
          setState({
            status: 'error',
            message: err instanceof Error ? err.message : String(err),
            path: '/api/baseline',
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return state;
}

export function usePin(): LoadState<PinDto> {
  const [state, setState] = useState<LoadState<PinDto>>({ status: 'loading' });

  useEffect(() => {
    let cancelled = false;
    fetchPin()
      .then((data) => {
        if (!cancelled) setState({ status: 'ok', data });
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        if (err instanceof ArtefactError) {
          setState({ status: 'error', message: err.message, path: err.path });
        } else {
          setState({
            status: 'error',
            message: err instanceof Error ? err.message : String(err),
            path: '/api/pin',
          });
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return state;
}
