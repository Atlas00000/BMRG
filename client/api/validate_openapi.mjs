/**
 * Minimal OpenAPI path presence check (no external YAML parser).
 * Run: node api/validate_openapi.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const specPath = path.join(root, 'openapi.yaml');
const text = fs.readFileSync(specPath, 'utf8');

const required = [
  '/health/latest:',
  '/baseline:',
  '/pin:',
  '/ledger:',
  '/jobs:',
  '/auth:',
  '/prove/cf:',
  'openapi: 3.',
];

const missing = required.filter((r) => !text.includes(r));
if (missing.length) {
  console.error('OpenAPI validation FAILED. Missing:', missing.join(', '));
  process.exit(1);
}

console.log('OpenAPI validation OK:', path.relative(process.cwd(), specPath));
console.log('Endpoints:', required.filter((r) => r.startsWith('/')).map((r) => r.replace(':', '')).join(', '));
