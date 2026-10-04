import type { ReactNode } from 'react';
import { Text } from '../primitives';
import './ActionRail.css';

type Props = {
  title?: string;
  children: ReactNode;
};

/** Vertical action cluster — replaces equal boxed toolbars. */
export function ActionRail({ title = 'Actions', children }: Props) {
  return (
    <aside className="ln-action-rail" aria-label={title}>
      <Text as="div" variant="label" tone="faint">
        {title}
      </Text>
      <div className="ln-action-rail__stack">{children}</div>
    </aside>
  );
}
