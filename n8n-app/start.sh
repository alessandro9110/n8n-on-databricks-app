#!/usr/bin/env bash
set -euo pipefail

# Change to the src/app directory where package.json is located
cd src/app

# Install dependencies if node_modules missing
if [ ! -d "node_modules" ]; then
  echo "[start.sh] node_modules missing. Running npm install..."
  npm install --omit=dev
fi

# Export listen vars for n8n
export N8N_LISTEN_ADDRESS="0.0.0.0"
export N8N_PORT="${DATABRICKS_APP_PORT:-${N8N_PORT:-5678}}"

echo "[start.sh] Launching n8n on ${N8N_LISTEN_ADDRESS}:${N8N_PORT}";
node start.js
