import { modeTone, zoneTone } from '../../design/backendMap';
import { useBaseline } from '../api/hooks';
import { fetchBlotterCurrent, fetchLiveJournal, fetchLiveStatus } from '../api/client';
import { useAsync } from '../api/useAsync';
import { PageEnter } from '../components/motion';
import { EmptyState, SkeletonMetricStrip } from '../components/patterns';
import { Badge, Surface, Text } from '../components/primitives';
import { PageFrame } from '../components/shells';
import {
  bookFromLive,
  filterJournalLines,
  formatPulseFromPointer,
  nextActionCopy,
  parseBlotterCurrent,
  productModeLabel,
} from '../lib/productCopy';

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
  const book = bookFromLive(live.status === 'ok' ? live.data : null);

  const nextAction =
    live.status === 'ok'
      ? nextActionCopy({
          attached: Boolean(live.data.attached),
          mode,
          book,
          fuses,
        })
      : 'Desk feed unavailable — confirm the attach, then reload.';

  const pointer = blotter.status === 'ok' ? parseBlotterCurrent(blotter.data) : null;
  const pulseFromPointer = pointer ? formatPulseFromPointer(pointer) : '';
  const pulseFromJournal =
    journal.status === 'ok'
      ? filterJournalLines(journal.data.lines, 1)[0]
      : null;
  const pulse =
    pulseFromPointer ||
    (pulseFromJournal ? `${pulseFromJournal.t} · ${pulseFromJournal.msg}` : '') ||
    'No scored day yet.';

  const strategy =
    baseline.status === 'ok' ? String(baseline.data.engine.role ?? 'Harvest') : 'Harvest';
  const market =
    live.status === 'ok'
      ? `${String(live.data.symbol ?? '—')} ${String(live.data.timeframe ?? '')}`.trim()
      : baseline.status === 'ok'
        ? `${baseline.data.engine.symbol ?? 'EURUSD'} ${baseline.data.engine.timeframe ?? 'M5'}`
        : '—';
  const account =
    live.status === 'ok'
      ? `${String(live.data.account_kind ?? '—')} · ${String(live.data.account ?? '—')}`
      : '—';
  const version = live.status === 'ok' ? `v${String(live.data.ea_version ?? '—')}` : '';

  return (
    <PageFrame
      eyebrow="Home"
      title="Operator glance"
      description="Champion health and the next step — one composition."
    >
      {live.status === 'loading' && baseline.status === 'loading' ? <SkeletonMetricStrip /> : null}
      {live.status === 'error' && baseline.status === 'error' ? (
        <EmptyState title="Champion data unavailable" detail="Reload once the desk feed is ready." />
      ) : null}

      <PageEnter delay={1}>
        <Surface className="ln-section ln-home-compose" accent="signal" aria-label="Champion glance">
          <div className="ln-home-compose__head">
            <Text as="h2" variant="title" className="ln-home-compose__title">
              {strategy}
              {version ? ` · ${version}` : ''}
            </Text>
            <div className="ln-chip-row">
              <Badge tone={modeTone(mode)}>{productModeLabel(mode)}</Badge>
              <Badge tone={posture.tone}>{posture.label}</Badge>
              {baseline.status === 'ok' ? (
                <Badge tone={zoneTone(baseline.data.health.zone)}>{baseline.data.health.zone}</Badge>
              ) : null}
            </div>
          </div>

          <dl className="ln-kv ln-home-compose__meta">
            <dt>Account</dt>
            <dd>{account}</dd>
            <dt>Market</dt>
            <dd>{market}</dd>
            <dt>Book</dt>
            <dd>
              {book.entries > 0 ? `${book.side} · ${book.entries}` : 'Flat'}
            </dd>
          </dl>

          {baseline.status === 'error' ? (
            <EmptyState title="Edge scores unavailable" detail="Reference book cannot be loaded." />
          ) : null}
          {baseline.status === 'ok' ? (
            <div className="ln-metric-row" aria-label="Edge metrics">
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
          ) : null}

          <div className="ln-home-compose__foot">
            <div>
              <Text as="div" variant="label" tone="faint">
                Next
              </Text>
              <Text as="p" variant="body">
                {nextAction}
              </Text>
            </div>
            <div>
              <Text as="div" variant="label" tone="faint">
                Last scored
              </Text>
              <Text as="p" variant="micro" tone="muted">
                {pulse}
              </Text>
            </div>
          </div>
        </Surface>
      </PageEnter>
    </PageFrame>
  );
}
