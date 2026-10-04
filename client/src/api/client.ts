import {
  adaptAuth,
  adaptBaseline,
  adaptCfScorecard,
  adaptHealthLatest,
  adaptJob,
  adaptLedgerCsv,
  adaptPin,
  type AuthDto,
  type BaselineDto,
  type CfProveDto,
  type HealthLatestDto,
  type JobDto,
  type LedgerDto,
  type PinDto,
} from '../../api/adapters/artefacts';

export class ArtefactError extends Error {
  path: string;
  status: number;

  constructor(message: string, path: string, status: number) {
    super(message);
    this.name = 'ArtefactError';
    this.path = path;
    this.status = status;
  }
}

/** Empty in Vite dev (fs_bridge). Set `VITE_API_BASE` for Railway / preview. */
const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined)?.replace(/\/$/, '') ?? '';

function apiUrl(path: string): string {
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  return `${API_BASE}${path}`;
}

async function getJson(url: string): Promise<Record<string, unknown>> {
  const res = await fetch(apiUrl(url));
  const body = (await res.json().catch(() => ({}))) as Record<string, unknown>;
  if (!res.ok) {
    throw new ArtefactError(
      String(body.detail ?? body.error ?? res.statusText),
      String(body.path ?? url),
      res.status,
    );
  }
  return body;
}

async function getText(url: string): Promise<{ text: string; pathHint: string }> {
  const res = await fetch(apiUrl(url));
  if (!res.ok) {
    const body = (await res.json().catch(() => ({}))) as Record<string, unknown>;
    throw new ArtefactError(
      String(body.detail ?? body.error ?? res.statusText),
      String(body.path ?? url),
      res.status,
    );
  }
  return { text: await res.text(), pathHint: url };
}

export async function fetchBaseline(): Promise<BaselineDto> {
  return adaptBaseline(await getJson('/api/baseline'));
}

export async function fetchHealthLatest(): Promise<HealthLatestDto> {
  return adaptHealthLatest(await getJson('/api/health/latest'));
}

export async function fetchPin(): Promise<PinDto> {
  return adaptPin(await getJson('/api/pin'));
}

export async function fetchPinShadow(): Promise<PinDto> {
  return adaptPin(await getJson('/api/pin/shadow'));
}

export async function fetchPinPrior(): Promise<PinDto> {
  return adaptPin(await getJson('/api/pin/prior'));
}

export async function fetchJobs(): Promise<JobDto> {
  return adaptJob(await getJson('/api/jobs'));
}

export async function fetchAuth(role: 'Viewer' | 'Operator' = 'Viewer'): Promise<AuthDto> {
  return adaptAuth(await getJson('/api/auth'), role);
}

export async function fetchCfProve(): Promise<CfProveDto> {
  return adaptCfScorecard(await getJson('/api/prove/cf'));
}

export async function fetchLedger(magic = 8210204): Promise<LedgerDto> {
  const { text, pathHint } = await getText(`/api/ledger?magic=${magic}`);
  return adaptLedgerCsv(text, magic, pathHint);
}

export async function fetchLiveStatus(): Promise<Record<string, unknown>> {
  return getJson('/api/live/status');
}

export async function fetchLiveJournal(): Promise<{
  source: string;
  path_hint: string;
  lines: { t: string; level: string; msg: string }[];
}> {
  const raw = await getJson('/api/live/journal');
  return {
    source: String(raw.source ?? ''),
    path_hint: String(raw.path_hint ?? ''),
    lines: Array.isArray(raw.lines)
      ? (raw.lines as { t: string; level: string; msg: string }[])
      : [],
  };
}

export async function fetchSkipAuditMd(): Promise<string> {
  const { text } = await getText('/api/prove/skip-audit');
  return text;
}

export async function fetchPromoteDryRun(): Promise<Record<string, unknown>> {
  return getJson('/api/ops/promote/dry-run');
}

export async function fetchCorrelation(): Promise<string> {
  const { text } = await getText('/api/ops/correlation');
  return text;
}

export async function fetchBlotterCurrent(): Promise<string> {
  const { text } = await getText('/api/blotter/current');
  return text;
}

export async function fetchBlotterIndex(): Promise<{
  current_path: string;
  inbox: unknown[];
  archives: { task_id: string; path: string; verdict: string }[];
}> {
  const raw = await getJson('/api/blotter/index');
  return {
    current_path: String(raw.current_path ?? ''),
    inbox: Array.isArray(raw.inbox) ? raw.inbox : [],
    archives: Array.isArray(raw.archives)
      ? (raw.archives as { task_id: string; path: string; verdict: string }[])
      : [],
  };
}
