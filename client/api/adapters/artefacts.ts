/**
 * UI-P1 artefact adapters — map INF JSON → console DTOs.
 * Paths relative to Experts/BMRG (AGENT_PATHS).
 */

export type HealthVectorDto = {
  n: number;
  wr_pct: number;
  ef_pp: number;
  e_n: number;
  bm_pp: number | null;
  leak_pp: number | null;
  zone: string;
  maxdd_pp: number | null;
  magic: number | null;
  source: string;
  r?: number | null;
  bwr_pct?: number | null;
  fires_90d_band?: [number, number] | null;
  note?: string | null;
};

export type WindowId = 'long' | 'stress_3M' | 'ytd';

export type WindowHealthDto = {
  id: WindowId;
  label: string;
  start: string | null;
  end: string | null;
  available: boolean;
  health: HealthVectorDto;
  note?: string | null;
};

export type IterationBarDto = {
  n_remaining_min: number;
  n_warn_below: number;
  w250_ef_floor_pp: number;
  w250_maxdd_slack_pp: number;
  fires_warn_below_pct: number;
  fires_stall_below_pct: number;
};

export type BaselineDto = {
  baseline_id: string;
  health: HealthVectorDto;
  windows: WindowHealthDto[];
  iteration_bar: IterationBarDto;
  engine: {
    role?: string;
    magic_champion?: number;
    preset_id?: string;
    ea_hint?: string;
    symbol?: string;
    timeframe?: string;
  };
  raw: Record<string, unknown>;
};

export type PinDto = {
  semver: string;
  mode: string;
  promoted_at: string | null;
  operator_waiver: boolean;
  source: string;
};

export type HealthLatestDto = {
  recipe: string;
  pass: boolean;
  source: string;
  raw: Record<string, unknown>;
};

export type JobDto = {
  job_id: string;
  status: string;
  verdict: string | null;
  started_at: string | null;
  source: string;
  raw: Record<string, unknown>;
};

export type AuthDto = {
  role: 'Viewer' | 'Operator';
  authorised: boolean;
  allows: string[];
  forbids_unless_extra_auth: string[];
  ea_version: string | null;
  model: string | null;
  note: string | null;
  can_mutate: boolean;
};

export type CfProveDto = {
  engine_ef_pp: number | null;
  cf_ef_pp: number | null;
  engine_n: number | null;
  cf_n: number | null;
  n_skipped: number | null;
  maxdd_engine: number | null;
  maxdd_cf: number | null;
  verdict: string | null;
  source: string;
};

export type LedgerDto = {
  kind: string;
  path: string;
  magic: number | null;
  preview_rows: Record<string, string>[];
  rows: Record<string, string>[];
  source: string;
};

function num(v: unknown, fallback = 0): number {
  const n = typeof v === 'number' ? v : Number(v);
  return Number.isFinite(n) ? n : fallback;
}

function str(v: unknown, fallback = ''): string {
  return v == null ? fallback : String(v);
}

export function adaptBaseline(raw: Record<string, unknown>): BaselineDto {
  const engine = (raw.engine ?? {}) as Record<string, unknown>;
  const windows = (raw.windows ?? {}) as Record<string, unknown>;
  const long = (windows.long ?? {}) as Record<string, unknown>;
  const stress = (windows.stress_3M ?? {}) as Record<string, unknown>;
  const costs = (raw.costs ?? {}) as Record<string, unknown>;
  const bar = (raw.iteration_bar ?? {}) as Record<string, unknown>;
  const magic = engine.magic_champion == null ? null : num(engine.magic_champion);
  const source = 'infra/baselines/ENGINE_BASELINE_v1.json';
  const leakDefault = num(costs.leak_proxy_pp, 2.2);

  const longHealth: HealthVectorDto = {
    n: num(long.n),
    wr_pct: num(long.wr_pct),
    ef_pp: num(long.ef_pp),
    e_n: num(long.e_n),
    bm_pp: long.bm_pp == null ? null : num(long.bm_pp),
    leak_pp: long.leak_pp == null ? leakDefault : num(long.leak_pp),
    zone: str(long.zone, 'Unknown'),
    maxdd_pp: long.maxdd_pp == null ? null : num(long.maxdd_pp),
    magic,
    source,
    r: long.r == null ? null : num(long.r),
    bwr_pct: long.bwr_pct == null ? null : num(long.bwr_pct),
    fires_90d_band: Array.isArray(long.fires_90d_band)
      ? [num(long.fires_90d_band[0]), num(long.fires_90d_band[1])]
      : null,
  };

  const stressHealth: HealthVectorDto = {
    n: num(stress.n),
    wr_pct: num(stress.wr_pct),
    ef_pp: num(stress.ef_pp),
    e_n: num(stress.e_n),
    bm_pp: null,
    leak_pp: leakDefault,
    zone: str(stress.zone, 'Unknown'),
    maxdd_pp: null,
    magic,
    source,
    r: 1,
    bwr_pct: stress.bwr_pct == null ? null : num(stress.bwr_pct),
    fires_90d_band: null,
    note: stress.n_note == null ? null : str(stress.n_note),
  };

  const ytdUnavailable: HealthVectorDto = {
    n: 0,
    wr_pct: 0,
    ef_pp: 0,
    e_n: 0,
    bm_pp: null,
    leak_pp: null,
    zone: 'Unavailable',
    maxdd_pp: null,
    magic,
    source,
    note: 'YTD not frozen in ENGINE_BASELINE_v1 — supply via eval artefact later',
  };

  const windowList: WindowHealthDto[] = [
    {
      id: 'long',
      label: 'Long',
      start: long.start == null ? null : str(long.start),
      end: long.end == null ? null : str(long.end),
      available: true,
      health: longHealth,
    },
    {
      id: 'stress_3M',
      label: 'Stress 3M',
      start: stress.start == null ? null : str(stress.start),
      end: stress.end == null ? null : str(stress.end),
      available: true,
      health: stressHealth,
      note: stress.n_note == null ? null : str(stress.n_note),
    },
    {
      id: 'ytd',
      label: 'YTD',
      start: null,
      end: null,
      available: false,
      health: ytdUnavailable,
      note: ytdUnavailable.note,
    },
  ];

  const iteration_bar: IterationBarDto = {
    n_remaining_min: num(bar.n_remaining_min, 100),
    n_warn_below: num(bar.n_warn_below, 385),
    w250_ef_floor_pp: num(bar.w250_ef_floor_pp, 0.77),
    w250_maxdd_slack_pp: num(bar.w250_maxdd_slack_pp, 2),
    fires_warn_below_pct: num(bar.fires_warn_below_pct_of_baseline, 70),
    fires_stall_below_pct: num(bar.fires_stall_below_pct_of_baseline, 50),
  };

  return {
    baseline_id: str(raw.baseline_id, 'ENGINE_BASELINE_v1'),
    health: longHealth,
    windows: windowList,
    iteration_bar,
    engine: {
      role: engine.role == null ? undefined : str(engine.role),
      magic_champion: magic == null ? undefined : magic,
      preset_id: engine.preset_id == null ? undefined : str(engine.preset_id),
      symbol: engine.symbol == null ? undefined : str(engine.symbol),
      timeframe: engine.timeframe == null ? undefined : str(engine.timeframe),
    },
    raw,
  };
}

export function adaptHealthLatest(raw: Record<string, unknown>): HealthLatestDto {
  const pytest = (raw.pytest ?? {}) as Record<string, unknown>;
  const artefacts = (raw.artefacts ?? {}) as Record<string, unknown>;
  const pass = Boolean(pytest.pass ?? artefacts.pass ?? raw.pass);
  return {
    recipe: str(raw.recipe, 'unknown'),
    pass,
    source: 'infra/artefacts/reports/LATEST_EVAL.json',
    raw,
  };
}

export function adaptPin(raw: Record<string, unknown>): PinDto {
  return {
    semver: str(raw.live_semver ?? raw.shadow_semver ?? raw.semver, 'unknown'),
    mode: str(raw.mode, raw.shadow_semver ? 'SHADOW' : 'OFF'),
    promoted_at: raw.promoted_at == null ? null : str(raw.promoted_at),
    operator_waiver: Boolean(raw.operator_waiver),
    source: str(raw.path, 'infra/artefacts/models/L2skip/PIN.json'),
  };
}

export function adaptJob(raw: Record<string, unknown>): JobDto {
  const result = (raw.result ?? {}) as Record<string, unknown>;
  return {
    job_id: str(raw.job_id, 'unknown'),
    status: str(raw.status, 'unknown'),
    verdict: result.verdict == null ? null : str(result.verdict),
    started_at: raw.started_at == null ? null : str(raw.started_at),
    source: 'infra/artefacts/queue/LATEST_JOB.json',
    raw,
  };
}

export function adaptAuth(
  raw: Record<string, unknown>,
  role: 'Viewer' | 'Operator' = 'Viewer',
): AuthDto {
  const allows = Array.isArray(raw.allows) ? raw.allows.map(String) : [];
  const forbids = Array.isArray(raw.forbids_unless_extra_auth)
    ? raw.forbids_unless_extra_auth.map(String)
    : [];
  const authorised = Boolean(raw.authorised);
  return {
    role,
    authorised,
    allows,
    forbids_unless_extra_auth: forbids,
    ea_version: raw.ea_version == null ? null : str(raw.ea_version),
    model: raw.model == null ? null : str(raw.model),
    note: raw.note == null ? null : str(raw.note),
    can_mutate: role === 'Operator' && authorised,
  };
}

export function authAllows(auth: AuthDto, action: string): boolean {
  if (!auth.can_mutate) return false;
  if (auth.forbids_unless_extra_auth.includes(action)) return false;
  return auth.allows.includes(action) || auth.allows.includes('*');
}

export function adaptCfScorecard(raw: Record<string, unknown>): CfProveDto {
  const cf = (raw.cf ?? raw) as Record<string, unknown>;
  const engineBlock = (cf.engine ?? {}) as Record<string, unknown>;
  const counter = (cf.counterfactual ?? {}) as Record<string, unknown>;
  const engineHv = (engineBlock.health_vector ?? {}) as Record<string, unknown>;
  const cfHv = (counter.health_vector ?? {}) as Record<string, unknown>;

  return {
    engine_ef_pp: engineHv.ef_pp == null ? null : num(engineHv.ef_pp),
    cf_ef_pp: cfHv.ef_pp == null ? null : num(cfHv.ef_pp),
    engine_n: engineHv.n == null ? (engineBlock.n == null ? null : num(engineBlock.n)) : num(engineHv.n),
    cf_n: cfHv.n == null ? (counter.n == null ? null : num(counter.n)) : num(cfHv.n),
    n_skipped: counter.n_skipped == null ? null : num(counter.n_skipped),
    maxdd_engine: engineBlock.maxdd_pp == null ? null : num(engineBlock.maxdd_pp),
    maxdd_cf: counter.maxdd_pp == null ? null : num(counter.maxdd_pp),
    verdict: cf.verdict == null ? null : str(cf.verdict),
    source: 'infra/artefacts/reports/INF-P4-T04_cf_scorecard.json',
  };
}

export function adaptLedgerCsv(csvText: string, magic: number | null, path: string): LedgerDto {
  const lines = csvText.trim().split(/\r?\n/);
  const header = (lines[0] ?? '').split(',');
  const parseLine = (line: string) => {
    const cols = line.split(',');
    const row: Record<string, string> = {};
    header.forEach((h, i) => {
      row[h.trim()] = (cols[i] ?? '').trim();
    });
    return row;
  };
  const rows = lines.slice(1).filter(Boolean).map(parseLine);
  return {
    kind: 'skip_or_aos_ledger',
    path,
    magic,
    preview_rows: rows.slice(0, 5),
    rows,
    source: path,
  };
}
