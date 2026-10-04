import { useAuth } from '../api/AuthContext';
import { fetchBlotterCurrent, fetchBlotterIndex } from '../api/client';
import { useAsync } from '../api/useAsync';
import { PageEnter } from '../components/motion';
import { EmptyState, SkeletonMetricStrip } from '../components/patterns';
import { Badge, Button, Surface, Text } from '../components/primitives';
import { PageFrame } from '../components/shells';
import { AuthGate } from '../features/auth/AuthGate';
import { PRESET_CATALOG } from '../features/presets/catalog';

const REVIEW_CHECKLIST = [
  'Scores reviewed for the active task',
  'Archive copy filed under the task name',
  'Inbox cleared so the next drop cannot mix',
  'Current pointer updated',
  'Do not purge the archive unless asked',
] as const;

const ATTACH_CHECKLIST = [
  'Chart: EURUSD M5 · expert attached',
  'Champion Live-hold preset loaded',
  'Kill off unless intentionally stopping',
  'Journal and ledger paths confirmed',
  'Demo attach is not a completed forward-test programme',
] as const;

const FT_METRICS = [
  { id: 'EF', note: 'Primary edge language' },
  { id: 'E_N', note: 'Sample-adjusted edge' },
  { id: 'MaxDD', note: 'Drawdown vs hard stop' },
  { id: 'Pace', note: 'Baskets / fire count — not confidence' },
  { id: 'Halt path', note: 'Equity / daily / hard-stop events' },
] as const;

function presetStackLabel(stack: string): string {
  if (stack.includes('PAPER')) return 'Paper';
  if (stack.includes('AOS') || stack.includes('LIVE')) return 'Protected';
  if (stack.includes('export')) return 'Export';
  if (stack.includes('Not OS')) return 'Secondary';
  return 'Engine';
}

export function Records() {
  const current = useAsync(() => fetchBlotterCurrent(), []);
  const index = useAsync(() => fetchBlotterIndex(), []);
  const { allows, auth, setRole } = useAuth();
  const ftLive = allows('AOS_LIVE_FT');

  return (
    <PageFrame
      eyebrow="Records"
      title="Runs & library"
      description="Pointers, archives, presets, and forward-test prep — mutate stays gated."
      actions={
        <div className="ln-chip-row">
          <Button
            variant={auth?.role === 'Viewer' ? 'primary' : 'ghost'}
            onClick={() => setRole('Viewer')}
          >
            Viewer
          </Button>
          <Button
            variant={auth?.role === 'Operator' ? 'primary' : 'ghost'}
            onClick={() => setRole('Operator')}
          >
            Operator
          </Button>
        </div>
      }
    >
      {(current.status === 'loading' || index.status === 'loading') && <SkeletonMetricStrip />}

      <PageEnter delay={1}>
        <Surface className="ln-section" accent="signal">
          <Text as="div" variant="label" tone="faint">
            Current pointer
          </Text>
          {current.status === 'error' ? (
            <EmptyState title="Pointer missing" detail="No current review pointer." />
          ) : current.status === 'ok' ? (
            <pre className="ln-journal" style={{ whiteSpace: 'pre-wrap' }}>
              {current.data}
            </pre>
          ) : null}
        </Surface>
      </PageEnter>

      <PageEnter delay={2}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Inbox
          </Text>
          {index.status === 'ok' ? (
            <Text as="p" tone="muted">
              {index.data.inbox.length === 0
                ? 'Inbox empty — ready for the next drop.'
                : `${index.data.inbox.length} unprocessed item(s).`}
            </Text>
          ) : index.status === 'error' ? (
            <EmptyState title="Inbox unavailable" detail="Cannot read inbox state." />
          ) : null}
        </Surface>
      </PageEnter>

      <PageEnter delay={3}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Archive
          </Text>
          {index.status === 'ok' ? (
            <table className="ln-table">
              <thead>
                <tr>
                  <th>task</th>
                  <th>verdict</th>
                </tr>
              </thead>
              <tbody>
                {index.data.archives.map((a) => (
                  <tr key={a.task_id}>
                    <td>{a.task_id}</td>
                    <td>
                      <Badge tone="ok">{a.verdict}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : null}
        </Surface>
      </PageEnter>

      <PageEnter delay={4}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Preset library
          </Text>
          <table className="ln-table">
            <thead>
              <tr>
                <th>role</th>
                <th>kind</th>
              </tr>
            </thead>
            <tbody>
              {PRESET_CATALOG.map((p) => (
                <tr key={p.role}>
                  <td>{p.role}</td>
                  <td>
                    <Badge tone={presetStackLabel(p.stack) === 'Paper' ? 'skip' : 'signal'}>
                      {presetStackLabel(p.stack)}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Surface>
      </PageEnter>

      <PageEnter delay={5}>
        <Surface className="ln-section">
          <Text as="div" variant="label" tone="faint">
            Forward-test prep
          </Text>
          <Badge tone={ftLive ? 'ok' : 'halt'}>{ftLive ? 'Programme open' : 'Blocked'}</Badge>
          <Text as="p" variant="micro" tone="muted">
            Attach checklist and metrics contract. Programme mutate stays blocked without extra
            authorisation.
          </Text>
          <ol style={{ margin: '0.5rem 0 0', paddingLeft: '1.1rem' }}>
            {ATTACH_CHECKLIST.map((item) => (
              <li key={item} style={{ marginBottom: '0.35rem' }}>
                <Text as="span" variant="micro" tone="muted">
                  {item}
                </Text>
              </li>
            ))}
          </ol>
          <table className="ln-table" style={{ marginTop: '0.75rem' }}>
            <thead>
              <tr>
                <th>field</th>
                <th>rule</th>
              </tr>
            </thead>
            <tbody>
              {FT_METRICS.map((m) => (
                <tr key={m.id}>
                  <td>{m.id}</td>
                  <td>{m.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <AuthGate action="AOS_LIVE_FT" title="Forward-test ship" fallback={null}>
            <div className="ln-chip-row" style={{ marginTop: '0.75rem' }}>
              <Button variant="primary">Register window</Button>
              <Button variant="ghost">Export sign-off</Button>
            </div>
          </AuthGate>
          {!ftLive ? (
            <Text as="p" variant="micro" tone="warn" style={{ marginTop: '0.75rem' }}>
              Role={auth?.role ?? '…'} cannot unlock forward-test ship while it remains forbidden.
            </Text>
          ) : null}
        </Surface>
      </PageEnter>

      <PageEnter delay={6}>
        <Surface className="ln-section" elevation="plane2">
          <Text as="div" variant="label" tone="faint">
            Review checklist
          </Text>
          <ol style={{ margin: '0.5rem 0 0', paddingLeft: '1.1rem' }}>
            {REVIEW_CHECKLIST.map((item) => (
              <li key={item} style={{ marginBottom: '0.4rem' }}>
                <Text as="span" variant="micro" tone="muted">
                  {item}
                </Text>
              </li>
            ))}
          </ol>
        </Surface>
      </PageEnter>
    </PageFrame>
  );
}
