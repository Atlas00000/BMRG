import { decisionTone, verdictTone } from '../../design/backendMap';
import {
  fetchCfProve,
  fetchLedger,
  fetchLiveStatus,
} from '../api/client';
import { useAsync } from '../api/useAsync';
import { PageEnter } from '../components/motion';
import { EmptyState, SkeletonMetricStrip } from '../components/patterns';
import { Badge, Button, Surface, Text } from '../components/primitives';
import { PageFrame } from '../components/shells';
import { downloadCsv, downloadJson } from '../lib/export';
import {
  productDecisionLabel,
  productVerdictLabel,
} from '../lib/productCopy';

const VERDICTS = [
  { at: '2026-09-27', label: 'Offline prove', verdict: 'ACCEPT' },
  { at: '2026-09-28', label: 'Hold-back audit', verdict: 'USER_GO' },
  { at: '2026-09-28', label: 'Live-hold ship', verdict: 'ACCEPT' },
] as const;

const PROTECTION = [
  { name: 'Entry hold-back', status: 'On' },
  { name: 'Hard stop / drawdown', status: 'On' },
  { name: 'Size modulator', status: 'On' },
  { name: 'Decision ledger', status: 'On' },
  { name: 'Sleeve throttle', status: 'Paper' },
  { name: 'Early-path abort', status: 'Paper' },
  { name: 'Session soft veto', status: 'Paper' },
  { name: 'Promotion desk', status: 'Offline' },
] as const;

export function Review() {
  const ledger = useAsync(() => fetchLedger(8210204), []);
  const cf = useAsync(() => fetchCfProve(), []);
  const live = useAsync(() => fetchLiveStatus(), []);
  const fuses =
    live.status === 'ok'
      ? ((live.data.fuses ?? {}) as Record<string, unknown>)
      : null;

  const rows =
    ledger.status === 'ok'
      ? ledger.data.rows.length
        ? ledger.data.rows
        : ledger.data.preview_rows
      : [];

  return (
    <PageFrame
      eyebrow="Review"
      title="Decisions & honesty"
      description="What was allowed or held back — and why offline prove is not live equity."
      actions={
        <>
          <Button
            variant="ghost"
            disabled={ledger.status !== 'ok'}
            onClick={() =>
              ledger.status === 'ok' && downloadCsv('review_decisions.csv', ledger.data.rows)
            }
          >
            Export decisions
          </Button>
          <Button
            variant="ghost"
            disabled={cf.status !== 'ok'}
            onClick={() => cf.status === 'ok' && downloadJson('review_prove.json', cf.data)}
          >
            Export prove
          </Button>
        </>
      }
    >
      {(ledger.status === 'loading' || cf.status === 'loading') && <SkeletonMetricStrip />}

      <PageEnter delay={1}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Decision feed
          </Text>
          {ledger.status === 'error' ? (
            <EmptyState title="Decision feed unavailable" detail="No recent allow/hold rows." />
          ) : (
            <table className="ln-table">
              <thead>
                <tr>
                  <th>event</th>
                  <th>outcome</th>
                  <th>reason</th>
                </tr>
              </thead>
              <tbody>
                {rows.slice(0, 14).map((r, i) => (
                  <tr key={i}>
                    <td>{r.event_id ?? '—'}</td>
                    <td>
                      <Badge tone={decisionTone(r.decision ?? '')}>
                        {productDecisionLabel(r.decision)}
                      </Badge>
                    </td>
                    <td>{r.reason_code ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Surface>
      </PageEnter>

      <PageEnter delay={2}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Protection map
          </Text>
          <div className="ln-chip-row">
            {PROTECTION.map((p) => (
              <Badge
                key={p.name}
                tone={
                  p.status === 'On' ? 'signal' : p.status === 'Paper' ? 'skip' : 'neutral'
                }
              >
                {p.name} · {p.status}
              </Badge>
            ))}
          </div>
        </Surface>
      </PageEnter>

      <PageEnter delay={3}>
        <Surface className="ln-section" accent="warn">
          <Text as="div" variant="label" tone="faint">
            Paper vs live
          </Text>
          <Text as="p" tone="muted">
            Offline prove can show a lift when held-back entries are removed from the paper book.
            That is not a live equity forecast — deposit, halt latch, and window start can diverge on
            the chart path.
          </Text>
          {cf.status === 'ok' ? (
            <div className="ln-metric-row">
              <div className="ln-metric">
                <Text as="div" variant="label" tone="faint">
                  Engine EF
                </Text>
                <Text as="div" variant="mono">
                  {cf.data.engine_ef_pp ?? '—'}
                </Text>
              </div>
              <div className="ln-metric">
                <Text as="div" variant="label" tone="faint">
                  Paper EF
                </Text>
                <Text as="div" variant="mono">
                  {cf.data.cf_ef_pp ?? '—'}
                </Text>
              </div>
              <div className="ln-metric">
                <Text as="div" variant="label" tone="faint">
                  Held back
                </Text>
                <Text as="div" variant="mono">
                  {cf.data.n_skipped ?? '—'}
                </Text>
              </div>
            </div>
          ) : null}
        </Surface>
      </PageEnter>

      <PageEnter delay={4}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Verdict timeline
          </Text>
          <table className="ln-table">
            <thead>
              <tr>
                <th>when</th>
                <th>review</th>
                <th>verdict</th>
              </tr>
            </thead>
            <tbody>
              {VERDICTS.map((v) => (
                <tr key={v.label}>
                  <td>{v.at}</td>
                  <td>{v.label}</td>
                  <td>
                    <Badge tone={verdictTone(v.verdict)}>
                      {productVerdictLabel(v.verdict)}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Surface>
      </PageEnter>

      <PageEnter delay={5}>
        <Surface className="ln-section" accent={fuses?.l3_halt ? 'halt' : 'none'}>
          <Text as="div" variant="label" tone="faint">
            Size & halt story
          </Text>
          {fuses ? (
            <>
              <dl className="ln-kv">
                <dt>Size</dt>
                <dd>×{String(fuses.f_mult)}</dd>
                <dt>Hard-stop</dt>
                <dd>{fuses.l3_halt ? 'Active' : 'Clear'}</dd>
                <dt>Equity / daily</dt>
                <dd>
                  {fuses.equity_halt || fuses.daily_loss_halt ? 'Latched' : 'Clear'}
                </dd>
              </dl>
              {fuses.note ? (
                <Text as="p" variant="micro" tone="warn">
                  {String(fuses.note)}
                </Text>
              ) : (
                <Text as="p" variant="micro" tone="muted">
                  No size/halt note on the current desk feed.
                </Text>
              )}
            </>
          ) : (
            <EmptyState title="Size story unavailable" detail="Live fuses not loaded." />
          )}
        </Surface>
      </PageEnter>

      <PageEnter delay={6}>
        <Surface className="ln-section" elevation="plane2">
          <Text as="div" variant="label" tone="faint">
            Export
          </Text>
          <Text as="p" variant="micro" tone="muted">
            Download decisions or prove packet for the archive — use Records to file the review.
          </Text>
        </Surface>
      </PageEnter>
    </PageFrame>
  );
}
