# Script di avvio locale n8n con configurazione Unity Catalog

# Requisiti: Node.js >=20.19 <25, npm install già eseguito

Write-Host "Avvio n8n con configurazione Unity Catalog locale..." -ForegroundColor Green

# Crea cartella locale per simulare Unity Catalog volume
$localN8nPath = ".\n8n_data"
if (!(Test-Path $localN8nPath)) {
    New-Item -ItemType Directory -Path $localN8nPath -Force
    Write-Host "Creata cartella locale: $localN8nPath" -ForegroundColor Yellow
}

# Variabili di configurazione base
$env:N8N_USER_FOLDER = (Resolve-Path $localN8nPath).Path
$env:GENERIC_TIMEZONE = "Europe/Rome"
$env:DB_TYPE = "sqlite"

# Fix warning: pool per SQLite
$env:DB_SQLITE_POOL_SIZE = "5"

# Fix warning: task runners abilitati
$env:N8N_RUNNERS_ENABLED = "true"

# Fix warning: accesso env in Code Node
$env:N8N_BLOCK_ENV_ACCESS_IN_NODE = "false"

# Fix warning: Git Node bare repo
$env:N8N_GIT_NODE_DISABLE_BARE_REPOS = "false"

Write-Host "Variabili impostate:" -ForegroundColor Cyan
Write-Host "  N8N_USER_FOLDER: $env:N8N_USER_FOLDER"
Write-Host "  DB_TYPE: $env:DB_TYPE"
Write-Host ""
Write-Host "Avvio n8n su http://localhost:5678 ..." -ForegroundColor Green

# Avvio n8n
npx n8n