import type { ReactNode } from 'react';
import { Text } from '../primitives';
import { NumberTick } from '../motion';
import './MetricStrip.css';

export type MetricItem = {
  id: string;
  label: string;
  value: number | string;
  hint?: string;
  format?: (v: number | string) => string;
};

type Props = {
  items: MetricItem[];
  trailing?: ReactNode;
};

/** Asymmetric metric ribbon — not equal cards. */
export function MetricStrip({ items, trailing }: Props) {
  return (
    <div className="ln-metric-strip" role="group" aria-label="Metrics">
      {items.map((item, i) => (
        <div
          key={item.id}
          className={['ln-metric-strip__cell', i === 0 ? 'is-lead' : ''].filter(Boolean).join(' ')}
        >
          <Text as="div" variant="label" tone="faint">
            {item.label}
          </Text>
          <Text as="div" variant="metric" className={i === 0 ? 'ln-metric-strip__lead-value' : ''}>
            <NumberTick value={item.value} format={item.format} />
          </Text>
          {item.hint ? (
            <Text as="div" variant="micro" tone="muted">
              {item.hint}
            </Text>
          ) : null}
        </div>
      ))}
      {trailing ? <div className="ln-metric-strip__trailing">{trailing}</div> : null}
    </div>
  );
}
