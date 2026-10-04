import type { HTMLAttributes, ReactNode } from 'react';
import type { Tone } from '../../../design/tokens';
import './Badge.css';

type Props = HTMLAttributes<HTMLSpanElement> & {
  tone?: Tone;
  children?: ReactNode;
};

export function Badge({ tone = 'neutral', className = '', children, ...rest }: Props) {
  const classes = ['ln-badge', `ln-badge--${tone}`, 'ln-state-crossfade', className]
    .filter(Boolean)
    .join(' ');
  return (
    <span className={classes} {...rest}>
      {children}
    </span>
  );
}
