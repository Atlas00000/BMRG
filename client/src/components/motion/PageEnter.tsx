import type { ReactNode } from 'react';

type Props = {
  children: ReactNode;
  delay?: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  className?: string;
};

export function PageEnter({ children, delay = 0, className = '' }: Props) {
  const delayClass = delay > 0 ? `ln-page-enter-delay-${delay}` : '';
  return (
    <div className={['ln-page-enter', delayClass, className].filter(Boolean).join(' ')}>
      {children}
    </div>
  );
}
