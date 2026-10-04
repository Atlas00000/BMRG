import path from 'node:path';
import { fileURLToPath } from 'node:url';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import { artefactBridgePlugin } from './api/fs_bridge.ts';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const bmrgRoot = path.resolve(__dirname, '..');

export default defineConfig(({ command }) => ({
  // Dev-only FS bridge. Production / Vercel uses VITE_API_BASE → Railway.
  plugins: [react(), ...(command === 'serve' ? [artefactBridgePlugin(bmrgRoot)] : [])],
  resolve: {
    alias: {
      '@api': path.resolve(__dirname, 'api'),
      '@design': path.resolve(__dirname, 'design'),
    },
  },
  server: {
    fs: {
      allow: [bmrgRoot],
    },
  },
}));
