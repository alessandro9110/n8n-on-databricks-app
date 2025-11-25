// Simple Node starter that runs n8n binding to the Databricks App port.
// Uses DATABRICKS_APP_PORT if available, otherwise falls back to 5678.

import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';

const port = process.env.DATABRICKS_APP_PORT || process.env.N8N_PORT || '5678';
const host = process.env.N8N_LISTEN_ADDRESS || '0.0.0.0';

// Resolve local n8n binary (avoid reliance on npx which may be absent in runtime)
const candidateBins = [
  process.env.N8N_BIN,
  path.resolve(process.cwd(), 'node_modules', '.bin', 'n8n'),
  path.resolve(process.cwd(), 'node_modules', 'n8n', 'bin', 'n8n'),
].filter(Boolean);

let n8nBin = candidateBins.find(p => fs.existsSync(p));
if (!n8nBin) {
  console.error('[startup] n8n binary not found. Ensure `npm install` has been run. Searched:', candidateBins);
  process.exit(1);
}

const env = {
  ...process.env,
  N8N_PORT: port,
  N8N_LISTEN_ADDRESS: host,
};

console.log(`Starting n8n via ${n8nBin} on ${host}:${port}...`);

// Invoke through node - n8n uses N8N_LISTEN_ADDRESS env var instead of --host
const child = spawn('node', [n8nBin], {
  stdio: 'inherit',
  env,
});

child.on('exit', (code) => {
  console.log(`n8n exited with code ${code}`);
  process.exit(code ?? 0);
});

child.on('error', (err) => {
  console.error('Failed to start n8n:', err);
  process.exit(1);
});
