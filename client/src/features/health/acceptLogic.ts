import type { HealthVectorDto, IterationBarDto, WindowHealthDto } from '../../../api/adapters/artefacts';
import type { Tone } from '../../../design/tokens';

export type GateStatus = 'pass' | 'warn' | 'fail' | 'na';

export type AcceptCheck = {
  id: string;
  label: string;
  status: GateStatus;
  detail: string;
};

export type DeltaRow = {
  id: string;
  label: string;
  value: string;
  tone: Tone;
  hint?: string;
};

export function gateTone(status: GateStatus): Tone {
  if (status === 'pass') return 'ok';
  if (status === 'warn') return 'warn';
  if (status === 'fail') return 'halt';
  return 'neutral';
}

/** Deltas of selected window vs locked long baseline (+ floors). */
export function buildBaselineDeltas(
  selected: WindowHealthDto,
  long: HealthVectorDto,
  bar: IterationBarDto,
): DeltaRow[] {
  if (!selected.available) {
    return [
      {
        id: 'na',
        label: 'Δ vs long',
        value: 'n/a',
        tone: 'neutral',
        hint: selected.note ?? 'Window artefact missing',
      },
    ];
  }

  const efDelta = selected.health.ef_pp - long.ef_pp;
  const enDelta = selected.health.e_n - long.e_n;
  const nDelta = selected.health.n - long.n;
  const vsFloor = selected.health.ef_pp - bar.w250_ef_floor_pp;

  return [
    {
      id: 'ef',
      label: 'Δ EF vs long',
      value: `${efDelta >= 0 ? '+' : ''}${efDelta.toFixed(2)} pp`,
      tone: efDelta >= 0 ? 'ok' : 'warn',
      hint: `long ${long.ef_pp.toFixed(2)}`,
    },
    {
      id: 'en',
      label: 'Δ E_N vs long',
      value: `${enDelta >= 0 ? '+' : ''}${enDelta.toFixed(3)} R`,
      tone: enDelta >= 0 ? 'ok' : 'warn',
    },
    {
      id: 'n',
      label: 'Δ n vs long',
      value: `${nDelta >= 0 ? '+' : ''}${nDelta}`,
      tone: selected.health.n >= bar.n_remaining_min ? 'ok' : 'halt',
    },
    {
      id: 'floor',
      label: 'EF − W250 floor',
      value: `${vsFloor >= 0 ? '+' : ''}${vsFloor.toFixed(2)} pp`,
      tone: vsFloor >= 0 ? 'ok' : 'halt',
      hint: `floor ${bar.w250_ef_floor_pp.toFixed(2)}`,
    },
  ];
}

export function buildAcceptChecks(
  selected: WindowHealthDto,
  long: HealthVectorDto,
  bar: IterationBarDto,
): AcceptCheck[] {
  if (!selected.available) {
    return [
      {
        id: 'window',
        label: 'Window data',
        status: 'na',
        detail: selected.note ?? 'No artefact for this window',
      },
    ];
  }

  const h = selected.health;
  const nStatus: GateStatus =
    h.n >= bar.n_warn_below ? 'pass' : h.n >= bar.n_remaining_min ? 'warn' : 'fail';

  const efStatus: GateStatus = h.ef_pp >= bar.w250_ef_floor_pp ? 'pass' : 'fail';

  const maxddStatus: GateStatus = h.maxdd_pp == null ? 'na' : 'pass';

  let firesStatus: GateStatus = 'na';
  let firesDetail = 'No fires band on this window';
  if (h.fires_90d_band) {
    const mid = (h.fires_90d_band[0] + h.fires_90d_band[1]) / 2;
    const vsLongBand = long.fires_90d_band
      ? mid / ((long.fires_90d_band[0] + long.fires_90d_band[1]) / 2)
      : 1;
    const pct = vsLongBand * 100;
    firesStatus =
      pct >= bar.fires_warn_below_pct ? 'pass' : pct >= bar.fires_stall_below_pct ? 'warn' : 'fail';
    firesDetail = `band ${h.fires_90d_band[0]}–${h.fires_90d_band[1]} / 90d (~${pct.toFixed(0)}% of long mid)`;
  } else if (selected.id === 'stress_3M') {
    firesStatus = h.n < bar.n_remaining_min ? 'warn' : 'pass';
    firesDetail = `thin-n stress · n=${h.n} (warn not kill)`;
  }

  return [
    {
      id: 'n',
      label: 'n remaining',
      status: nStatus,
      detail: `n=${h.n} · min ${bar.n_remaining_min} · warn < ${bar.n_warn_below}`,
    },
    {
      id: 'ef',
      label: 'EF vs floor',
      status: efStatus,
      detail: `EF ${h.ef_pp.toFixed(2)} ≥ floor ${bar.w250_ef_floor_pp.toFixed(2)} (W250 bar proxy)`,
    },
    {
      id: 'maxdd',
      label: 'MaxDD slack',
      status: maxddStatus,
      detail:
        h.maxdd_pp == null
          ? 'Unmeasured on baseline — +2pp slack applies when measured'
          : `MaxDD ${h.maxdd_pp.toFixed(1)}% · slack +${bar.w250_maxdd_slack_pp} pp`,
    },
    {
      id: 'fires',
      label: 'Fires vs baseline',
      status: firesStatus,
      detail: firesDetail,
    },
  ];
}

export function overallAccept(checks: AcceptCheck[]): GateStatus {
  if (checks.some((c) => c.status === 'fail')) return 'fail';
  if (checks.some((c) => c.status === 'warn')) return 'warn';
  if (checks.every((c) => c.status === 'na')) return 'na';
  return 'pass';
}
