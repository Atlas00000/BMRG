import type { ReactNode } from 'react';
import { PageEnter } from '../motion';
import { PageHeader } from './PageHeader';
import '../../styles/page.css';

type Props = {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
  children: ReactNode;
};

/** Shared stage frame for the five product pages. */
export function PageFrame({ eyebrow, title, description, actions, children }: Props) {
  return (
    <PageEnter>
      <div className="ln-page">
        <PageHeader
          eyebrow={eyebrow}
          title={title}
          description={description}
          actions={actions}
        />
        <div className="ln-page__sections">{children}</div>
      </div>
    </PageEnter>
  );
}
