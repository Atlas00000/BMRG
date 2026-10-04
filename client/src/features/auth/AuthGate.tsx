import type { ReactNode } from 'react';
import { useAuth } from '../../api/AuthContext';
import { EmptyState } from '../../components/patterns';
import { Surface, Text } from '../../components/primitives';

type Props = {
  action: string;
  title?: string;
  /** When denied, render this instead of default EmptyState. Pass null to hide. */
  fallback?: ReactNode | null;
  children: ReactNode;
};

/** Hard wall: children render only when authAllows(action). */
export function AuthGate({ action, title = 'Gated', fallback, children }: Props) {
  const { allows, auth, loading } = useAuth();

  if (loading) {
    return (
      <Surface>
        <Text as="p" tone="faint">
          Checking authorisation…
        </Text>
      </Surface>
    );
  }

  if (!allows(action)) {
    if (fallback === null) return null;
    if (fallback !== undefined) return <>{fallback}</>;
    return (
      <EmptyState
        title={`${title} locked`}
        detail={`Requires WIRE allow for ${action}. Role=${auth?.role ?? 'none'} · currently blocked (forbids_unless_extra_auth or Viewer).`}
      />
    );
  }

  return <>{children}</>;
}
