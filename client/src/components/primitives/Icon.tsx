import type { HTMLAttributes, ReactNode, SVGProps } from 'react';
import './Icon.css';

type Props = HTMLAttributes<HTMLSpanElement> & {
  size?: number;
  label?: string;
  children?: ReactNode;
};

/** Wrapper only — pass an inline SVG child. No emoji / clip-art. */
export function Icon({ size = 16, label, className = '', children, ...rest }: Props) {
  return (
    <span
      className={['ln-icon', className].filter(Boolean).join(' ')}
      style={{ width: size, height: size }}
      role={label ? 'img' : 'presentation'}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      {...rest}
    >
      {children}
    </span>
  );
}

export function IconMark(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" {...props}>
      <path d="M4 7h16M4 12h10M4 17h7" strokeLinecap="square" />
      <path d="M18 14l3 3-3 3" strokeLinecap="square" />
    </svg>
  );
}
