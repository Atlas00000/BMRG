import { useEffect, useRef, useState } from 'react';

type Props = {
  value: number | string;
  className?: string;
  format?: (v: number | string) => string;
};

/** Brief opacity tick when the displayed value changes. */
export function NumberTick({ value, className = '', format }: Props) {
  const [flash, setFlash] = useState(false);
  const prev = useRef(value);

  useEffect(() => {
    if (prev.current === value) return;
    prev.current = value;
    const reduce =
      typeof window !== 'undefined' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;
    setFlash(true);
    const t = window.setTimeout(() => setFlash(false), 320);
    return () => window.clearTimeout(t);
  }, [value]);

  const shown = format ? format(value) : String(value);

  return (
    <span
      className={['ln-number-tick', className].filter(Boolean).join(' ')}
      style={{ opacity: flash ? 0.45 : 1 }}
    >
      {shown}
    </span>
  );
}
