import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import { authAllows, type AuthDto } from '../../api/adapters/artefacts';
import { ArtefactError, fetchAuth } from './client';

type AuthContextValue = {
  auth: AuthDto | null;
  loading: boolean;
  error: string | null;
  errorPath: string | null;
  setRole: (role: 'Viewer' | 'Operator') => void;
  refresh: () => void;
  allows: (action: string) => boolean;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [role, setRole] = useState<'Viewer' | 'Operator'>('Viewer');
  const [auth, setAuth] = useState<AuthDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [errorPath, setErrorPath] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchAuth(role)
      .then((dto) => {
        if (cancelled) return;
        setAuth(dto);
        setError(null);
        setErrorPath(null);
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        if (err instanceof ArtefactError) {
          setError(err.message);
          setErrorPath(err.path);
        } else {
          setError(err instanceof Error ? err.message : String(err));
          setErrorPath('/api/auth');
        }
        setAuth(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [role, tick]);

  const refresh = useCallback(() => setTick((t) => t + 1), []);

  const value = useMemo<AuthContextValue>(
    () => ({
      auth,
      loading,
      error,
      errorPath,
      setRole,
      refresh,
      allows: (action: string) => (auth ? authAllows(auth, action) : false),
    }),
    [auth, loading, error, errorPath, refresh],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth requires AuthProvider');
  return ctx;
}
