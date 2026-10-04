/**
 * Kyoto Ledger + Matcha Iron — typed token names.
 * CSS source of truth: ./tokens.css
 * Palette: ./APP_THEME.md §5
 */
export const color = {
  canvas: 'var(--ln-canvas)',
  plane: 'var(--ln-plane)',
  plane2: 'var(--ln-plane-2)',
  hairline: 'var(--ln-hairline)',
  hairlineStrong: 'var(--ln-hairline-strong)',
  ink: 'var(--ln-ink)',
  inkMuted: 'var(--ln-ink-muted)',
  inkFaint: 'var(--ln-ink-faint)',
  signal: 'var(--ln-signal)',
  signalDim: 'var(--ln-signal-dim)',
  warn: 'var(--ln-warn)',
  halt: 'var(--ln-halt)',
  ok: 'var(--ln-ok)',
  skip: 'var(--ln-skip)',
} as const;

export const space = {
  0: 'var(--ln-space-0)',
  1: 'var(--ln-space-1)',
  2: 'var(--ln-space-2)',
  3: 'var(--ln-space-3)',
  4: 'var(--ln-space-4)',
  5: 'var(--ln-space-5)',
  6: 'var(--ln-space-6)',
  7: 'var(--ln-space-7)',
  8: 'var(--ln-space-8)',
} as const;

export const radius = {
  sm: 'var(--ln-radius-sm)',
  md: 'var(--ln-radius-md)',
  lg: 'var(--ln-radius-lg)',
} as const;

export const duration = {
  fast: 'var(--ln-dur-fast)',
  base: 'var(--ln-dur-base)',
  slow: 'var(--ln-dur-slow)',
} as const;

export const ease = {
  out: 'var(--ln-ease-out)',
} as const;

export type Tone = 'neutral' | 'signal' | 'ok' | 'warn' | 'halt' | 'skip';
