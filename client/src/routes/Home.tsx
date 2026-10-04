import { modeTone, zoneTone } from '../../design/backendMap';
import { useBaseline } from '../api/hooks';
import { fetchBlotterCurrent, fetchLiveJournal, fetchLiveStatus } from '../api/client';
import { useAsync } from '../api/useAsync';
import { PageEnter } from '../components/motion';
import { EmptyState, SkeletonMetricStrip } from '../components/patterns';
import { Badge, Surface, Text } from '../components/primitives';
import { PageFrame } from '../components/shells';
import { productModeLabel } from '../lib/productCopy';

function postureFromLive(fuses: Record<string, unknown> | null, mode: string): {
  label: string;
  tone: 'ok' | 'signal' | 'warn' | 'halt' | 'skip';
} {
  if (!fuses) return { label: 'Status unavailable', tone: 'warn' };
  if (fuses.l3_halt || fuses.equity_halt || fuses.daily_loss_halt) {
    return { label: 'Halt — new entries stopped', tone: 'halt' };
  }
  if (fuses.pause) return { label: 'Paused', tone: 'warn' };
  const m = productModeLabel(mode);
  if (m === 'Live-hold') return { label: 'Live-hold — some entries held back', tone: 'signal' };
  if (m === 'Observe-only') return { label: 'Observe-only — logging, not holding', tone: 'skip' };
  return { label: 'Protection off — engine only', tone: 'ok' };
}

export function Home() {
  const baseline = useBaseline();
  const live = useAsync(() => fetchLiveStatus(), []);
  const journal = useAsync(() => fetchLiveJournal(), []);
  const blotter = useAsync(() => fetchBlotterCurrent(), []);

  const mode = live.status === 'ok' ? String(live.data.mode ?? '') : '';
  const fuses =
    live.status === 'ok' ? ((live.data.fuses ?? null) as Record<string, unknown> | null) : null;
  const posture = postureFromLive(fuses, mode);

  const nextAction =
    live.status === 'ok' && live.data.attached
      ? 'Keep the chart attach running, then score today’s book under Performance when the session closes.'
      : 'Attach the champion preset on the chart, confirm Live-hold mode, then return here for the next step.';

  const pulse =
    blotter.status === 'ok'
      ? blotter.data.trim().split(/\r?\n/).filter(Boolean).slice(0, 3).join(' · ')
      : journal.status === 'ok' && journal.data.lines[0]
        ? `${journal.data.lines[0].t} · ${journal.data.lines[0].msg}`
        : 'No recent pulse yet.';

  return (
    <PageFrame
      eyebrow="Home"
      title="Operator glance"
      description="One composition: champion health and the next step — not a dashboard."
    >
      <section className="ln-section ln-home-hero" aria-label="Brand frame">
        <div className="ln-home-hero__brand">BMRG</div>
        <Text as="p" tone="muted">
          Read-first console for the Harvest champion.
        </Text>
      </section>

      <PageEnter delay={1}>
        <Surface className="ln-section" accent="signal">
          <Text as="div" variant="label" tone="faint" className="ln-section__title">
            Champion strip
          </Text>
          {live.status === 'loading' || baseline.status === 'loading' ? (
            <SkeletonMetricStrip />
          ) : null}
          {live.status === 'error' && baseline.status === 'error' ? (
            <EmptyState title="Champion data unavailable" detail="Reload once the desk feed is ready." />
          ) : (
            <dl className="ln-kv">
              <dt>Strategy</dt>
              <dd>
                {baseline.status === 'ok'
                  ? String(baseline.data.engine.role ?? 'Harvest')
                  : 'Harvest'}
              </dd>
              <dt>Account</dt>
              <dd>
                {live.status === 'ok'
                  ? `${String(live.data.account_kind ?? '—')} · ${String(live.data.account ?? '—')}`
                  : '—'}
              </dd>
              <dt>Version</dt>
              <dd>{live.status === 'ok' ? `v${String(live.data.ea_version ?? '—')}` : '—'}</dd>
              <dt>Market</dt>
              <dd>
                {live.status === 'ok'
                  ? `${String(live.data.symbol ?? '—')} ${String(live.data.timeframe ?? '')}`
                  : baseline.status === 'ok'
                    ? `${baseline.data.engine.symbol ?? 'EURUSD'} ${baseline.data.engine.timeframe ?? 'M5'}`
                    : '—'}
              </dd>
            </dl>
          )}
        </Surface>
      </PageEnter>

      <PageEnter delay={2}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Edge snapshot
          </Text>
          {baseline.status === 'loading' ? <SkeletonMetricStrip /> : null}
          {baseline.status === 'error' ? (
            <EmptyState title="Edge scores unavailable" detail="Reference book cannot be loaded." />
          ) : null}
          {baseline.status === 'ok' ? (
            <>
              <div className="ln-metric-row">
                <div className="ln-metric">
                  <Text as="div" variant="label" tone="faint">
                    EF
                  </Text>
                  <Text as="div" variant="metric">
                    {baseline.data.health.ef_pp.toFixed(2)}
                  </Text>
                </div>
                <div className="ln-metric">
                  <Text as="div" variant="label" tone="faint">
                    E_N
                  </Text>
                  <Text as="div" variant="metric">
                    {baseline.data.health.e_n >= 0 ? '+' : ''}
                    {baseline.data.health.e_n.toFixed(3)}R
                  </Text>
                </div>
                <div className="ln-metric">
                  <Text as="div" variant="label" tone="faint">
                    n
                  </Text>
                  <Text as="div" variant="metric">
                    {baseline.data.health.n}
                  </Text>
                </div>
                <div className="ln-metric">
                  <Text as="div" variant="label" tone="faint">
                    WR
                  </Text>
                  <Text as="div" variant="metric">
                    {baseline.data.health.wr_pct.toFixed(1)}%
                  </Text>
                </div>
              </div>
              <Badge tone={zoneTone(baseline.data.health.zone)}>{baseline.data.health.zone}</Badge>
            </>
          ) : null}
        </Surface>
      </PageEnter>

      <PageEnter delay={3}>
        <Surface className="ln-section" accent={posture.tone === 'halt' ? 'halt' : 'none'}>
          <Text as="div" variant="label" tone="faint">
            Protection posture
          </Text>
          <div className="ln-chip-row">
            <Badge tone={modeTone(mode)}>{productModeLabel(mode)}</Badge>
            <Badge tone={posture.tone}>{posture.label}</Badge>
          </div>
        </Surface>
      </PageEnter>

      <PageEnter delay={4}>
        <Surface className="ln-section" elevation="plane2">
          <Text as="div" variant="label" tone="faint">
            Next action
          </Text>
          <Text as="p" variant="body">
            {nextAction}
          </Text>
        </Surface>
      </PageEnter>

      <PageEnter delay={5}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Recent pulse
          </Text>
          <Text as="p" variant="micro" tone="muted">
            {pulse}
          </Text>
        </Surface>
      </PageEnter>
    </PageFrame>
  );
}
