import type { ReactNode } from 'react';
import { Text } from '../primitives';
import './PageHeader.css';

type Props = {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
};

export function PageHeader({ eyebrow, title, description, actions }: Props) {
  return (
    <header className="ln-page-header">
      <div className="ln-page-header__copy">
        {eyebrow ? (
          <Text as="div" variant="label" tone="signal">
            {eyebrow}
          </Text>
        ) : null}
        <Text as="h1" variant="display">
          {title}
        </Text>
        {description ? (
          <Text as="p" tone="muted" className="ln-page-header__desc">
            {description}
          </Text>
        ) : null}
      </div>
      {actions ? <div className="ln-page-header__actions">{actions}</div> : null}
    </header>
  );
}
