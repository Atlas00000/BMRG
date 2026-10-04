import fs from 'node:fs';
import path from 'node:path';
import type { ServerResponse } from 'node:http';
import type { Plugin } from 'vite';

type ArtefactRef = { root: 'infra' | 'bmrg' | 'client'; parts: string[]; type?: 'json' | 'text' | 'csv' | 'md' | 'jsonl' };

/** OpenAPI-aligned artefact map (Experts/BMRG relative). */
export const ARTEFACT_FILES: Record<string, ArtefactRef> = {
  '/api/baseline': { root: 'infra', parts: ['baselines', 'ENGINE_BASELINE_v1.json'] },
  '/api/health/latest': { root: 'infra', parts: ['artefacts', 'reports', 'LATEST_EVAL.json'] },
  '/api/pin': { root: 'infra', parts: ['artefacts', 'models', 'L2skip', 'LATEST_LIVE', 'PIN.json'] },
  '/api/pin/shadow': { root: 'infra', parts: ['artefacts', 'models', 'L2skip', 'LATEST_SHADOW', 'PIN.json'] },
  '/api/pin/prior': { root: 'infra', parts: ['artefacts', 'models', 'L2skip', 'LATEST_LIVE', 'PRIOR_PIN.json'] },
  '/api/jobs': { root: 'infra', parts: ['artefacts', 'queue', 'LATEST_JOB.json'] },
  '/api/auth': { root: 'infra', parts: ['artefacts', 'ops', 'WIRE_AUTHORISATION.json'] },
  '/api/prove/cf': { root: 'infra', parts: ['artefacts', 'reports', 'INF-P4-T04_cf_scorecard.json'] },
  '/api/prove/skip-audit': { root: 'infra', parts: ['INF-P6-T02_skip_audit.md'], type: 'md' },
  '/api/ledger': {
    root: 'infra',
    parts: ['artefacts', 'reports', 'skip_ledger', 'LATEST_SKIP_LEDGER.csv'],
    type: 'csv',
  },
  '/api/live/journal': { root: 'client', parts: ['fixtures', 'live', 'demo_journal.json'] },
  '/api/live/status': { root: 'client', parts: ['fixtures', 'live', 'demo_status.json'] },
  '/api/ops/promote/dry-run': { root: 'infra', parts: ['fixtures', 'promote', 'dry_run.json'] },
  '/api/ops/correlation': {
    root: 'infra',
    parts: ['artefacts', 'logs', 'LATEST_CORRELATION.jsonl'],
    type: 'jsonl',
  },
  '/api/blotter/current': { root: 'bmrg', parts: ['blotter', 'CURRENT.md'], type: 'md' },
  '/api/blotter/index': { root: 'client', parts: ['fixtures', 'blotter', 'archive_index.json'] },
};

function sendJson(res: ServerResponse, status: number, body: unknown) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(body));
}

function sendText(res: ServerResponse, status: number, body: string, type: string) {
  res.statusCode = status;
  res.setHeader('Content-Type', type);
  res.end(body);
}

function resolvePath(bmrgRoot: string, ref: ArtefactRef): string {
  if (ref.root === 'infra') return path.join(bmrgRoot, 'infra', ...ref.parts);
  if (ref.root === 'client') return path.join(bmrgRoot, 'client', ...ref.parts);
  return path.join(bmrgRoot, ...ref.parts);
}

export function artefactBridgePlugin(bmrgRoot: string): Plugin {
  return {
    name: 'bmrg-artefact-bridge',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split('?')[0] ?? '';
        if (!url.startsWith('/api/')) {
          next();
          return;
        }

        const ref = ARTEFACT_FILES[url];
        if (!ref) {
          // Let Vite serve source under client/api/** (adapters, openapi helpers).
          next();
          return;
        }

        const filePath = resolvePath(bmrgRoot, ref);
        if (!fs.existsSync(filePath)) {
          sendJson(res, 404, {
            error: 'artefact_missing',
            path: path.relative(bmrgRoot, filePath).replace(/\\/g, '/'),
            detail: 'Drop or generate the INF artefact, then reload.',
          });
          return;
        }

        try {
          const raw = fs.readFileSync(filePath);
          const text = raw.toString('utf8');
          const kind = ref.type ?? (filePath.endsWith('.csv') ? 'csv' : filePath.endsWith('.md') ? 'md' : filePath.endsWith('.jsonl') ? 'jsonl' : 'json');
          if (kind === 'csv') {
            sendText(res, 200, text, 'text/csv; charset=utf-8');
            return;
          }
          if (kind === 'md') {
            sendText(res, 200, text, 'text/markdown; charset=utf-8');
            return;
          }
          if (kind === 'jsonl') {
            sendText(res, 200, text, 'application/x-ndjson; charset=utf-8');
            return;
          }
          sendText(res, 200, text, 'application/json; charset=utf-8');
        } catch (err) {
          sendJson(res, 500, {
            error: 'read_failed',
            path: filePath,
            detail: err instanceof Error ? err.message : String(err),
          });
        }
      });
    },
  };
}
