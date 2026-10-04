import type { Tone } from './tokens';

/** Backend enums / literals → visual tone. Keep aligned with INF / AOS artefacts. */

export type ZoneId =
  | 'Fragile'
  | 'Strong_EF_thin_n'
  | 'Near frontier'
  | 'Stable'
  | string;

export type LifecycleId =
  | 'Stable'
  | 'Near frontier'
  | 'Below frontier'
  | 'Derisk'
  | 'Halt'
  | string;

export type DecisionId = 'FIRE' | 'ALLOW_UNCERTAIN' | 'SKIP' | 'FIRE_OK' | string;

export type AiOsModeId = 'OFF' | 'SHADOW' | 'LIVE_WITHHOLD' | 0 | 1 | 2 | string;

export type VerdictId = 'ACCEPT' | 'REJECT' | 'USER_GO' | 'GO' | 'NO-GO' | string;

export function zoneTone(zone: ZoneId): Tone {
  const z = String(zone);
  if (/strong|robust/i.test(z)) return 'ok';
  if (/near frontier/i.test(z)) return 'signal';
  if (/fragile|thin/i.test(z)) return 'warn';
  return 'neutral';
}

export function lifecycleTone(life: LifecycleId): Tone {
  const l = String(life);
  if (/halt/i.test(l)) return 'halt';
  if (/derisk|below/i.test(l)) return 'warn';
  if (/near frontier/i.test(l)) return 'signal';
  if (/stable/i.test(l)) return 'ok';
  return 'neutral';
}

export function decisionTone(decision: DecisionId): Tone {
  const d = String(decision).toUpperCase();
  if (d === 'SKIP' || d.includes('WOULD_SKIP')) return 'skip';
  if (d.includes('ALLOW_UNCERTAIN')) return 'warn';
  if (d.includes('FIRE')) return 'ok';
  return 'neutral';
}

export function modeTone(mode: AiOsModeId): Tone {
  const m = String(mode).toUpperCase();
  if (m === '2' || m === 'LIVE_WITHHOLD') return 'signal';
  if (m === '1' || m === 'SHADOW') return 'skip';
  return 'neutral';
}

export function verdictTone(verdict: VerdictId): Tone {
  const v = String(verdict).toUpperCase();
  if (v.includes('REJECT') || v.includes('NO-GO')) return 'halt';
  if (v.includes('ACCEPT') || v === 'GO' || v.includes('USER_GO')) return 'ok';
  return 'warn';
}

export function haltTone(halted: boolean): Tone {
  return halted ? 'halt' : 'ok';
}

export function modeLabel(mode: AiOsModeId): string {
  const m = String(mode).toUpperCase();
  if (m === '2' || m === 'LIVE_WITHHOLD') return 'LIVE_WITHHOLD';
  if (m === '1' || m === 'SHADOW') return 'SHADOW';
  if (m === '0' || m === 'OFF') return 'OFF';
  return String(mode);
}
