import { haltTone, modeTone } from '../../design/backendMap';
import { fetchLiveJournal, fetchLiveStatus } from '../api/client';
import { useAsync } from '../api/useAsync';
import { PageEnter } from '../components/motion';
import { EmptyState, SkeletonMetricStrip } from '../components/patterns';
import { Badge, Button, Surface, Text } from '../components/primitives';
import { PageFrame } from '../components/shells';
import { productModeLabel } from '../lib/productCopy';

export function Live() {
  const status = useAsync(() => fetchLiveStatus(), []);
  const journal = useAsync(() => fetchLiveJournal(), []);
  const fuses =
    status.status === 'ok'
      ? ((status.data.fuses ?? {}) as Record<string, unknown>)
      : null;

  return (
    <PageFrame
      eyebrow="Live"
      title="Desk"
      description="Observe the attached expert. Orders and kill stay on the chart — never in the browser."
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
            <Surface className="ln-section" accent="signal">
              <Text as="div" variant="label" tone="faint">
                Attachment
              </Text>
              <dl className="ln-kv">
                <dt>Market</dt>
                <dd>
                  {String(status.data.symbol)} {String(status.data.timeframe)}
                </dd>
                <dt>Preset</dt>
                <dd>{String(status.data.preset_id)}</dd>
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
            <Surface className="ln-section">
              <Text as="div" variant="label" tone="faint">
                Run mode
              </Text>
              <div className="ln-chip-row">
                <Badge tone={modeTone(String(status.data.mode))}>
                  {productModeLabel(String(status.data.mode))}
                </Badge>
                <Badge tone={status.data.kill_switch ? 'halt' : 'ok'}>
                  {status.data.kill_switch ? 'Kill on' : 'Kill off'}
                </Badge>
              </div>
              <Text as="p" variant="micro" tone="muted">
                Off · Observe-only · Live-hold. Change mode on chart inputs, not here.
              </Text>
            </Surface>
          </PageEnter>

          <PageEnter delay={3}>
            <Surface
              className="ln-section"
              accent={fuses?.l3_halt || fuses?.equity_halt ? 'halt' : 'none'}
            >
              <Text as="div" variant="label" tone="faint">
                Safety strip
              </Text>
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
            <Surface className="ln-section">
              <Text as="div" variant="label" tone="faint">
                Open book
              </Text>
              <dl className="ln-kv">
                <dt>Side</dt>
                <dd>None</dd>
                <dt>Entries</dt>
                <dd>0</dd>
                <dt>Exposure</dt>
                <dd>Flat</dd>
              </dl>
              <Text as="p" variant="micro" tone="faint">
                Read-only basket view — no modify or close from this console.
              </Text>
            </Surface>
          </PageEnter>

          <PageEnter delay={5}>
            <Surface className="ln-section">
              <Text as="div" variant="label" tone="faint">
                Journal
              </Text>
              {journal.status === 'ok' ? (
                <div className="ln-journal">
                  {journal.data.lines.map((line, i) => (
                    <p key={i} className="ln-journal__line">
                      <strong>{line.t}</strong> {line.msg}
                    </p>
                  ))}
                </div>
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
            <Surface className="ln-section" elevation="plane2">
              <Text as="div" variant="label" tone="faint">
                Desk notices
              </Text>
              <Text as="p" tone="muted">
                Kill switch is chart-side only. This console does not place, modify, or close orders.
              </Text>
              <div className="ln-chip-row">
                <Button variant="ghost" disabled>
                  Toggle kill (remote) — forbidden
                </Button>
                <Button variant="ghost" disabled>
                  Place order — forbidden
                </Button>
              </div>
            </Surface>
          </PageEnter>
        </>
      ) : null}
    </PageFrame>
  );
}
