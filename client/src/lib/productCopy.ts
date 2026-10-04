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
