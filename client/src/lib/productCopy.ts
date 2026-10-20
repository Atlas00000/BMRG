/** Product-facing labels — never expose internal mode enums in UI. */

export function productModeLabel(mode: string | number | undefined): string {
  const m = String(mode ?? '').toUpperCase();
  if (m === '2' || m === 'LIVE_WITHHOLD') return 'Live-hold';
  if (m === '1' || m === 'SHADOW') return 'Observe-only';
  if (m === '0' || m === 'OFF' || !m) return 'Off';
  return 'Off';
}

export function productDecisionLabel(decision: string | undefined): string {
  const d = String(decision ?? '').toUpperCase();
  if (d.includes('SKIP') || d.includes('WOULD_SKIP')) return 'Held back';
  if (d.includes('ALLOW')) return 'Allowed (uncertain)';
  if (d.includes('FIRE')) return 'Allowed';
  return decision ? String(decision) : '—';
}

export function productVerdictLabel(verdict: string): string {
  const v = verdict.toUpperCase();
  if (v.includes('REJECT') || v.includes('NO-GO')) return 'Reject';
  if (v.includes('USER_GO')) return 'Go (operator)';
  if (v.includes('ACCEPT') || v === 'GO') return 'Accept';
  return verdict;
}

/** Champion session window (broker/server clock) from INF-LIVE_WITHHOLD ddl30. */
export const SESSION = {
  startHour: 12,
  endHour: 20,
  /** day_of_week: 0=Sun … 6=Sat — Mon/Wed/Thu/Fri */
  tradeDays: [1, 3, 4, 5] as readonly number[],
} as const;

/**
 * Broker/server hour from wall clock.
 * Observed on YWO demo: server ≈ UTC when local is UTC+1.
 */
export function brokerNow(now = new Date()): { hour: number; day: number; minute: number } {
  return {
    hour: now.getUTCHours(),
    minute: now.getUTCMinutes(),
    day: now.getUTCDay(),
  };
}

export function inSession(now = new Date()): boolean {
  const { hour, day } = brokerNow(now);
  if (!SESSION.tradeDays.includes(day)) return false;
  return hour >= SESSION.startHour && hour < SESSION.endHour;
}

export type BlotterPointer = {
  taskId: string;
  archivedAt: string;
  verdict: string;
  archivePath: string;
  raw: string;
};

export function parseBlotterCurrent(text: string): BlotterPointer {
  const cleaned = text.replace(/^\uFEFF/, '').trim();
  const lines = cleaned.split(/\r?\n/).filter(Boolean);
  const map = new Map<string, string>();
  for (const line of lines) {
    const i = line.indexOf(':');
    if (i <= 0) continue;
    map.set(line.slice(0, i).trim().replace(/^\uFEFF/, ''), line.slice(i + 1).trim());
  }
  return {
    taskId: map.get('task_id') ?? '',
    archivedAt: map.get('archived_at') ?? '',
    verdict: map.get('verdict') ?? '',
    archivePath: map.get('archive_path') ?? '',
    raw: cleaned,
  };
}

/** Operator pulse from CURRENT.md — no raw YAML dump. */
export function formatPulseFromPointer(p: BlotterPointer): string {
  if (!p.taskId && !p.verdict) return '';
  const day = p.taskId.replace(/^LIVE-/, '').replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3');
  const parts = [day || p.taskId, p.verdict].filter(Boolean);
  return parts.join(' · ');
}

export type JournalLine = { t: string; level: string; msg: string };

const JOURNAL_KEEP =
  /\[TRADE\]|OPEN |close TP|close SL|AOS close|Entry blocked|Entry failed|init OK|AOS ON|halt|Flatten|equity halt|fail pause|WOULD_SKIP|L2INF/i;

/** Prefer operator-relevant lines; fall back to newest non-bar lines. */
export function filterJournalLines(lines: JournalLine[], limit = 5): JournalLine[] {
  const kept = lines.filter((l) => JOURNAL_KEEP.test(l.msg));
  if (kept.length) return kept.slice(-limit).reverse();
  const nonBar = lines.filter((l) => !/\bbar=/.test(l.msg) && !/sig=0 no signal/i.test(l.msg));
  const pool = nonBar.length ? nonBar : lines;
  return pool.slice(-limit).reverse();
}

export function bookFromLive(data: Record<string, unknown> | null): {
  side: string;
  entries: number;
  exposure: string;
} {
  const book = (data?.book ?? data?.basket ?? null) as Record<string, unknown> | null;
  if (!book) {
    return { side: 'None', entries: 0, exposure: 'Flat' };
  }
  const side = String(book.side ?? book.basket_side ?? 'None');
  const entries = Number(book.entries ?? book.n ?? book.entry_count ?? 0);
  const exposureRaw = book.exposure ?? book.exposure_pct;
  const exposure =
    exposureRaw == null || exposureRaw === ''
      ? entries > 0
        ? 'Open'
        : 'Flat'
      : typeof exposureRaw === 'number'
        ? `${exposureRaw}%`
        : String(exposureRaw);
  return {
    side: side === 'NONE' || side === '' ? 'None' : side,
    entries: Number.isFinite(entries) ? entries : 0,
    exposure: entries === 0 ? 'Flat' : exposure,
  };
}

export function nextActionCopy(opts: {
  attached: boolean;
  mode: string;
  book: { side: string; entries: number };
  fuses: Record<string, unknown> | null;
  now?: Date;
}): string {
  const { attached, mode, book, fuses, now = new Date() } = opts;
  if (!attached) {
    return 'Attach the champion Live-hold preset on EURUSD M5, then return here.';
  }
  if (fuses?.l3_halt || fuses?.equity_halt || fuses?.daily_loss_halt) {
    return 'Halt is latched — clear on the chart before expecting new entries.';
  }
  if (fuses?.pause) {
    return 'Fail-pause is active — wait for pause bars to clear, or check the chart journal.';
  }
  const { hour, day } = brokerNow(now);
  if (!SESSION.tradeDays.includes(day)) {
    return 'Weekday filter: no new entries today. Review the last scored day under Records.';
  }
  if (hour < SESSION.startHour) {
    return `Outside session (opens ${SESSION.startHour}:00 server). Watch Live for the first in-window signal.`;
  }
  if (hour >= SESSION.endHour) {
    return 'Session closed. Score today’s book under Performance, then file the review in Records.';
  }
  if (book.entries > 0) {
    return `In session · ${book.side} open (${book.entries}). Manage on the chart — console is observe-only.`;
  }
  const m = productModeLabel(mode);
  if (m === 'Live-hold') {
    return 'In session · flat · Live-hold on. Waiting for a band touch the gate allows.';
  }
  return `In session · flat · mode ${m}. Confirm Live-hold on the chart if you expect holds.`;
}

export function presetDisplayName(presetId: string | undefined): string {
  const id = String(presetId ?? '').trim();
  if (!id) return '—';
  return id
    .replace(/\.set$/i, '')
    .replace(/_/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}
