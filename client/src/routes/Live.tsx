import { haltTone, modeTone } from '../../design/backendMap';
import { fetchLiveJournal, fetchLiveStatus } from '../api/client';
import { useAsync } from '../api/useAsync';
import { PageEnter } from '../components/motion';
import { EmptyState, SkeletonMetricStrip } from '../components/patterns';
import { Badge, Surface, Text } from '../components/primitives';
import { PageFrame } from '../components/shells';
import {
  bookFromLive,
  filterJournalLines,
  presetDisplayName,
  productModeLabel,
} from '../lib/productCopy';

export function Live() {
  const status = useAsync(() => fetchLiveStatus(), []);
  const journal = useAsync(() => fetchLiveJournal(), []);
  const fuses =
    status.status === 'ok'
      ? ((status.data.fuses ?? {}) as Record<string, unknown>)
      : null;
  const book = bookFromLive(status.status === 'ok' ? status.data : null);
  const events =
    journal.status === 'ok' ? filterJournalLines(journal.data.lines, 5) : [];

  return (
    <PageFrame
      eyebrow="Live"
      title="Desk"
      description="Observe the attached expert. Orders and kill stay on the chart."
      actions={
        status.status === 'ok' ? (
          <Badge tone={modeTone(String(status.data.mode))}>
            {productModeLabel(String(status.data.mode))}
          </Badge>
        ) : null
      }
    >
      {status.status === 'loading' ? <SkeletonMetricStrip /> : null}
      {status.status === 'error' ? (
        <EmptyState title="Live desk unavailable" detail="Attach feed cannot be loaded." />
      ) : null}

      {status.status === 'ok' ? (
        <>
          <PageEnter delay={1}>
            <Surface className="ln-section" accent="signal" aria-label="Attachment">
              <Text as="h2" variant="title">
                {String(status.data.symbol)} {String(status.data.timeframe)}
              </Text>
              <dl className="ln-kv">
                <dt>Preset</dt>
                <dd>{presetDisplayName(String(status.data.preset_id))}</dd>
                <dt>Version</dt>
                <dd>v{String(status.data.ea_version)}</dd>
                <dt>Account</dt>
                <dd>
                  {String(status.data.account_kind)} · {String(status.data.account)}
                </dd>
                <dt>Attached</dt>
                <dd>{status.data.attached ? 'Yes' : 'No'}</dd>
              </dl>
            </Surface>
          </PageEnter>

          <PageEnter delay={2}>
            <Surface className="ln-section" aria-label="Run mode">
              <div className="ln-chip-row">
                <Badge tone={modeTone(String(status.data.mode))}>
                  {productModeLabel(String(status.data.mode))}
                </Badge>
                <Badge tone={status.data.kill_switch ? 'halt' : 'ok'}>
                  {status.data.kill_switch ? 'Kill on' : 'Kill off'}
                </Badge>
              </div>
              <Text as="p" variant="micro" tone="muted">
                Change mode on chart jobs — this console does not switch Live-hold.
              </Text>
            </Surface>
          </PageEnter>

          <PageEnter delay={3}>
            <Surface
              className="ln-section"
              accent={fuses?.l3_halt || fuses?.equity_halt ? 'halt' : 'none'}
              aria-label="Safety"
            >
              <div className="ln-chip-row">
                <Badge tone={haltTone(Boolean(fuses?.equity_halt))}>
                  Equity {fuses?.equity_halt ? 'halt' : 'clear'}
                </Badge>
                <Badge tone={haltTone(Boolean(fuses?.daily_loss_halt))}>
                  Daily {fuses?.daily_loss_halt ? 'halt' : 'clear'}
                </Badge>
                <Badge tone={haltTone(Boolean(fuses?.l3_halt))}>
                  Hard-stop {fuses?.l3_halt ? 'halt' : 'clear'}
                </Badge>
                <Badge tone={fuses?.pause ? 'warn' : 'ok'}>
                  {fuses?.pause ? 'Paused' : 'Running'}
                </Badge>
                <Badge tone={Number(fuses?.f_mult) < 1 ? 'warn' : 'ok'}>
                  Size ×{String(fuses?.f_mult ?? '—')}
                </Badge>
              </div>
            </Surface>
          </PageEnter>

          <PageEnter delay={4}>
            <Surface className="ln-section" aria-label="Open book">
              <dl className="ln-kv">
                <dt>Side</dt>
                <dd>{book.side}</dd>
                <dt>Entries</dt>
                <dd>{book.entries}</dd>
                <dt>Exposure</dt>
                <dd>{book.exposure}</dd>
              </dl>
              <Text as="p" variant="micro" tone="faint">
                Read-only basket — no modify or close from this console.
              </Text>
            </Surface>
          </PageEnter>

          <PageEnter delay={5}>
            <Surface className="ln-section" aria-label="Journal">
              {journal.status === 'ok' ? (
                events.length ? (
                  <div className="ln-journal">
                    {events.map((line, i) => (
                      <p key={`${line.t}-${i}`} className="ln-journal__line">
                        <strong>{line.t}</strong> {line.msg}
                      </p>
                    ))}
                  </div>
                ) : (
                  <Text as="p" tone="muted">
                    No recent opens, closes, or gate events in the feed.
                  </Text>
                )
              ) : journal.status === 'error' ? (
                <EmptyState title="Journal unavailable" detail="No recent desk lines." />
              ) : (
                <Text as="p" tone="faint">
                  Loading journal…
                </Text>
              )}
            </Surface>
          </PageEnter>

          <PageEnter delay={6}>
            <Surface className="ln-section" elevation="plane2" aria-label="Desk notices">
              <Text as="p" tone="muted">
                Kill switch and orders stay on the chart. This console never places, modifies, or
                closes positions.
              </Text>
            </Surface>
          </PageEnter>
        </>
      ) : null}
    </PageFrame>
  );
}
