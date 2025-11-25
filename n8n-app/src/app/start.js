// Simple Node starter that runs n8n binding to the Databricks App port.
// Uses DATABRICKS_APP_PORT if available, otherwise falls back to 5678.

import { spawn } from 'child_process';

const port = process.env.DATABRICKS_APP_PORT || process.env.N8N_PORT || '5678';
const host = process.env.N8N_LISTEN_ADDRESS || '0.0.0.0';

// Optional: set editor URL hints if provided via environment
// (prefer configuring these in the Databricks App UI for correctness)
const env = {
  ...process.env,
  N8N_PORT: port,
  N8N_LISTEN_ADDRESS: host,
};

console.log(`Starting n8n on ${host}:${port}...`);

const child = spawn('npx', ['n8n', '--host', host, '--port', port], {
  stdio: 'inherit',
  env,
  shell: false,
});

child.on('exit', (code) => {
  console.log(`n8n exited with code ${code}`);
  process.exit(code ?? 0);
});

child.on('error', (err) => {
  console.error('Failed to start n8n:', err);
  process.exit(1);
});
