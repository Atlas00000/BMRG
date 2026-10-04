import { Badge, Text } from '../../components/primitives';
import { StateCrossfade } from '../../components/motion';
import type { DeltaRow } from './acceptLogic';
import './BaselineDeltaStrip.css';

type Props = {
  rows: DeltaRow[];
  referenceLabel?: string;
};

export function BaselineDeltaStrip({ rows, referenceLabel = 'vs ENGINE_BASELINE long' }: Props) {
  return (
    <section className="ln-delta-strip" aria-label="Baseline deltas">
      <div className="ln-delta-strip__head">
        <Text as="div" variant="label" tone="faint">
          Baseline Δ
        </Text>
        <Text as="div" variant="micro" tone="muted">
          {referenceLabel}
        </Text>
      </div>
      <div className="ln-delta-strip__row">
        {rows.map((row) => (
          <div key={row.id} className="ln-delta-strip__cell">
            <Text as="div" variant="label" tone="faint">
              {row.label}
            </Text>
            <StateCrossfade stateKey={row.value}>
              <Text
                as="div"
                variant="metric"
                tone={row.tone === 'neutral' ? 'muted' : row.tone}
                className="ln-delta-strip__value"
              >
                {row.value}
              </Text>
            </StateCrossfade>
            {row.hint ? (
              <Text as="div" variant="micro" tone="faint">
                {row.hint}
              </Text>
            ) : null}
            <Badge tone={row.tone}>{row.tone}</Badge>
          </div>
        ))}
      </div>
    </section>
  );
}
