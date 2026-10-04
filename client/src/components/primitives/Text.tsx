import type { CSSProperties, HTMLAttributes, ReactNode } from 'react';
import './Text.css';

type Variant = 'display' | 'title' | 'body' | 'label' | 'micro' | 'mono' | 'metric';
type Tone = 'default' | 'muted' | 'faint' | 'signal' | 'ok' | 'warn' | 'halt' | 'skip';

type Props = HTMLAttributes<HTMLElement> & {
  as?: 'p' | 'span' | 'h1' | 'h2' | 'h3' | 'div' | 'label';
  variant?: Variant;
  tone?: Tone;
  children?: ReactNode;
};

export function Text({
  as: Tag = 'p',
  variant = 'body',
  tone = 'default',
  className = '',
  children,
  style,
  ...rest
}: Props) {
  const classes = ['ln-text', `ln-text--${variant}`, `ln-text--tone-${tone}`, className]
    .filter(Boolean)
    .join(' ');
  return (
    <Tag className={classes} style={style as CSSProperties} {...rest}>
      {children}
    </Tag>
  );
}
