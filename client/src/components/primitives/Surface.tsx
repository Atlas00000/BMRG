import type { CSSProperties, HTMLAttributes, ReactNode } from 'react';
import './Surface.css';

type Elevation = 'flat' | 'plane' | 'plane2';

type Props = HTMLAttributes<HTMLDivElement> & {
  children?: ReactNode;
  elevation?: Elevation;
  accent?: 'none' | 'signal' | 'warn' | 'halt';
  pad?: 'none' | 'sm' | 'md' | 'lg';
};

export function Surface({
  children,
  elevation = 'plane',
  accent = 'none',
  pad = 'md',
  className = '',
  style,
  ...rest
}: Props) {
  const classes = [
    'ln-surface',
    `ln-surface--${elevation}`,
    `ln-surface--pad-${pad}`,
    accent !== 'none' ? `ln-surface--accent-${accent}` : '',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={classes} style={style as CSSProperties} {...rest}>
      {children}
    </div>
  );
}
