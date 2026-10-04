import type { ReactNode } from 'react';

type Props = {
  stateKey: string | number | boolean;
  children: ReactNode;
  className?: string;
};

/** Crossfade container — CSS handles transition; key remounts content when state changes. */
export function StateCrossfade({ stateKey, children, className = '' }: Props) {
  return (
    <div key={String(stateKey)} className={['ln-state-crossfade', className].filter(Boolean).join(' ')}>
      {children}
    </div>
  );
}
