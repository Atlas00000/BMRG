import { Badge, Text } from '../../components/primitives';
import { StateCrossfade } from '../../components/motion';
import {
  gateTone,
  overallAccept,
  type AcceptCheck,
  type GateStatus,
} from './acceptLogic';
import './AcceptBar.css';

type Props = {
  checks: AcceptCheck[];
};

function statusLabel(s: GateStatus): string {
  if (s === 'pass') return 'PASS';
  if (s === 'warn') return 'WARN';
  if (s === 'fail') return 'FAIL';
  return 'N/A';
}

export function AcceptBar({ checks }: Props) {
  const overall = overallAccept(checks);

  return (
    <section className="ln-accept-bar" aria-label="Accept bar">
      <div className="ln-accept-bar__head">
        <Text as="div" variant="label" tone="faint">
          Accept bar
        </Text>
        <StateCrossfade stateKey={overall}>
          <Badge tone={gateTone(overall)}>overall {statusLabel(overall)}</Badge>
        </StateCrossfade>
      </div>
      <ul className="ln-accept-bar__list">
        {checks.map((c) => (
          <li key={c.id} className={`ln-accept-bar__item is-${c.status}`}>
            <div className="ln-accept-bar__item-top">
              <Text as="span" variant="label">
                {c.label}
              </Text>
              <Badge tone={gateTone(c.status)}>{statusLabel(c.status)}</Badge>
            </div>
            <Text as="p" variant="micro" tone="muted">
              {c.detail}
            </Text>
          </li>
        ))}
      </ul>
    </section>
  );
}
