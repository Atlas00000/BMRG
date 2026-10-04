import type { HealthVectorDto } from '../../../api/adapters/artefacts';
import { zoneTone } from '../../../design/backendMap';
import { Badge, Surface, Text } from '../../components/primitives';
import { NumberTick } from '../../components/motion';
import { MetricStrip } from '../../components/patterns';
import './HealthVectorPanel.css';

type Props = {
  health: HealthVectorDto;
  title?: string;
};

export function HealthVectorPanel({ health, title = 'Health vector' }: Props) {
  return (
    <Surface elevation="plane" accent="signal" className="ln-health-vector" pad="md">
      <div className="ln-health-vector__head">
        <Text as="div" variant="label" tone="faint">
          {title}
        </Text>
        <Badge tone={zoneTone(health.zone)}>{health.zone}</Badge>
      </div>

      <MetricStrip
        items={[
          {
            id: 'ef',
            label: 'EF pp',
            value: health.ef_pp,
            hint: health.source.split('/').pop(),
            format: (v) => Number(v).toFixed(2),
          },
          {
            id: 'en',
            label: 'E_N',
            value: health.e_n,
            format: (v) => {
              const n = Number(v);
              return `${n >= 0 ? '+' : ''}${n.toFixed(3)}R`;
            },
          },
          { id: 'n', label: 'n', value: health.n },
          {
            id: 'wr',
            label: 'WR',
            value: health.wr_pct,
            format: (v) => `${Number(v).toFixed(1)}%`,
          },
          {
            id: 'bm',
            label: 'BM',
            value: health.bm_pp ?? 0,
            format: (v) => (health.bm_pp == null ? '—' : `${Number(v).toFixed(1)} pp`),
          },
        ]}
        trailing={
          <div className="ln-health-vector__trail">
            <Text as="div" variant="micro" tone="faint">
              Leak
            </Text>
            <Text as="div" variant="metric" className="ln-health-vector__leak">
              <NumberTick
                value={health.leak_pp ?? 0}
                format={(v) => (health.leak_pp == null ? '—' : `${Number(v).toFixed(1)}`)}
              />
            </Text>
          </div>
        }
      />

      <div className="ln-health-vector__meta">
        <Text as="span" variant="mono" tone="muted">
          magic {health.magic ?? '—'}
        </Text>
        {health.r != null ? (
          <Text as="span" variant="micro" tone="muted">
            R={health.r}
          </Text>
        ) : null}
        {health.bwr_pct != null ? (
          <Text as="span" variant="micro" tone="muted">
            BWR {health.bwr_pct}%
          </Text>
        ) : null}
        {health.maxdd_pp != null ? (
          <Text as="span" variant="micro" tone="muted">
            MaxDD {health.maxdd_pp.toFixed(1)}%
          </Text>
        ) : (
          <Text as="span" variant="micro" tone="faint">
            MaxDD unmeasured
          </Text>
        )}
      </div>
    </Surface>
  );
}
