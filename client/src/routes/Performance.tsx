import { useMemo, useState } from 'react';
import type { WindowId } from '../../api/adapters/artefacts';
import { zoneTone } from '../../design/backendMap';
import { useBaseline } from '../api/hooks';
import { PageEnter } from '../components/motion';
import { EmptyState, SkeletonMetricStrip } from '../components/patterns';
import { Badge, Button, Surface, Text } from '../components/primitives';
import { PageFrame } from '../components/shells';
import {
  AcceptBar,
  BaselineDeltaStrip,
  buildAcceptChecks,
  buildBaselineDeltas,
} from '../features/health';

export function Performance() {
  const baseline = useBaseline();
  const [windowId, setWindowId] = useState<WindowId>('long');

  const selected = useMemo(() => {
    if (baseline.status !== 'ok') return null;
    return baseline.data.windows.find((w) => w.id === windowId) ?? baseline.data.windows[0];
  }, [baseline, windowId]);

  const longHealth = baseline.status === 'ok' ? baseline.data.health : null;
  const deltas =
    baseline.status === 'ok' && selected && longHealth
      ? buildBaselineDeltas(selected, longHealth, baseline.data.iteration_bar)
      : [];
  const checks =
    baseline.status === 'ok' && selected && longHealth
      ? buildAcceptChecks(selected, longHealth, baseline.data.iteration_bar)
      : [];

  const firesBand =
    baseline.status === 'ok' && Array.isArray(baseline.data.health.fires_90d_band)
      ? baseline.data.health.fires_90d_band
      : null;

  return (
    <PageFrame
      eyebrow="Performance"
      title="Edge of the book"
      description="Score windows the way the edge framework speaks — not vanity balance."
    >
      {baseline.status === 'loading' ? <SkeletonMetricStrip /> : null}
      {baseline.status === 'error' ? (
        <EmptyState title="Performance unavailable" detail="Reference scores cannot be loaded." />
      ) : null}

      {baseline.status === 'ok' && selected ? (
        <>
          <PageEnter delay={1}>
            <Surface className="ln-section">
              <Text as="div" variant="label" tone="faint">
                Window switcher
              </Text>
              <div className="ln-chip-row">
                {baseline.data.windows.map((w) => (
                  <Button
                    key={w.id}
                    variant={selected.id === w.id ? 'primary' : 'ghost'}
                    onClick={() => setWindowId(w.id)}
                  >
                    {w.label}
                    {!w.available ? ' · n/a' : ''}
                  </Button>
                ))}
              </div>
            </Surface>
          </PageEnter>

          <PageEnter delay={2}>
            <Surface className="ln-section" accent="signal">
              <Text as="div" variant="label" tone="faint">
                Edge scorecard · {selected.label}
              </Text>
              {selected.available ? (
                <>
                  <div className="ln-metric-row">
                    <div className="ln-metric">
                      <Text as="div" variant="label" tone="faint">
                        EF
                      </Text>
                      <Text as="div" variant="metric">
                        {selected.health.ef_pp.toFixed(2)}
                      </Text>
                    </div>
                    <div className="ln-metric">
                      <Text as="div" variant="label" tone="faint">
                        E_N
                      </Text>
                      <Text as="div" variant="metric">
                        {selected.health.e_n >= 0 ? '+' : ''}
                        {selected.health.e_n.toFixed(3)}R
                      </Text>
                    </div>
                    <div className="ln-metric">
                      <Text as="div" variant="label" tone="faint">
                        n
                      </Text>
                      <Text as="div" variant="metric">
                        {selected.health.n}
                      </Text>
                    </div>
                    <div className="ln-metric">
                      <Text as="div" variant="label" tone="faint">
                        WR
                      </Text>
                      <Text as="div" variant="metric">
                        {selected.health.wr_pct.toFixed(1)}%
                      </Text>
                    </div>
                    <div className="ln-metric">
                      <Text as="div" variant="label" tone="faint">
                        MaxDD
                      </Text>
                      <Text as="div" variant="metric">
                        {selected.health.maxdd_pp == null
                          ? '—'
                          : `${selected.health.maxdd_pp.toFixed(1)}%`}
                      </Text>
                    </div>
                  </div>
                  <Badge tone={zoneTone(selected.health.zone)}>{selected.health.zone}</Badge>
                </>
              ) : (
                <EmptyState
                  title={`${selected.label} not available`}
                  detail={selected.note ?? 'No freeze for this window yet.'}
                />
              )}
            </Surface>
          </PageEnter>

          <PageEnter delay={3}>
            <Surface className="ln-section">
              <Text as="div" variant="label" tone="faint">
                Vs reference
              </Text>
              <BaselineDeltaStrip rows={deltas} />
            </Surface>
          </PageEnter>

          <PageEnter delay={4}>
            <Surface className="ln-section">
              <Text as="div" variant="label" tone="faint">
                Accept posture
              </Text>
              <AcceptBar checks={checks} />
            </Surface>
          </PageEnter>

          <PageEnter delay={5}>
            <Surface className="ln-section">
              <Text as="div" variant="label" tone="faint">
                Activity cadence
              </Text>
              {firesBand ? (
                <Text as="p" tone="muted">
                  Expected pace about {firesBand[0]}–{firesBand[1]} baskets per 90 days — roughly
                  half to one basket on a typical session day. Quiet days are normal.
                </Text>
              ) : (
                <Text as="p" tone="muted">
                  Cadence band not published for this reference.
                </Text>
              )}
            </Surface>
          </PageEnter>

          <PageEnter delay={6}>
            <Surface className="ln-section" accent="warn">
              <Text as="div" variant="label" tone="faint">
                Caveats
              </Text>
              <Text as="p" tone="muted">
                Offline paper lift is not a live equity forecast. Path, deposit, and halt timing can
                diverge from the reference book — score the chart path on its own terms.
              </Text>
            </Surface>
          </PageEnter>
        </>
      ) : null}
    </PageFrame>
  );
}
