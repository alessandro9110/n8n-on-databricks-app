# n8n-app

## Getting Started

To deploy and manage this asset bundle, follow these steps:

### 1. Deployment

- Click the **deployment rocket** 🚀 in the left sidebar to open the **Deployments** panel, then click **Deploy**.

### 2. Running Jobs & Pipelines

- To run a deployed job or pipeline, hover over the resource in the **Deployments** panel and click the **Run** button.

### 3. Managing Resources

- Use the **Create** dropdown to add resources to the asset bundle.
- Click **Schedule** on a notebook within the asset bundle to create a **job definition** that schedules the notebook.

## Documentation

- For information on using **Databricks Asset Bundles in the workspace**, see: [Databricks Asset Bundles in the workspace](https://docs.databricks.com/aws/en/dev-tools/bundles/workspace-bundles)
- For details on the **Databricks Asset Bundles format** used in this asset bundle, see: [Databricks Asset Bundles Configuration reference](https://docs.databricks.com/aws/en/dev-tools/bundles/reference)

## n8n Application

Questa bundle ora avvia solo **n8n Community Edition** tramite il comando definito in `src/app/app.yaml` (`npx n8n`). L'interfaccia è disponibile sulla porta 5678.

### Requisiti Runtime

- **Node.js**: versione compresa tra **20.19** e **24.x** (inclusivo). Consigliato usare l'ultima LTS >= 20.19.
- Verifica locale con:

```bash
node -v
```

Se la versione è <20.19 aggiorna prima Node.js (su Windows usa installer ufficiale, su Databricks assicurati che l'ambiente abbia la versione richiesta prima dell'esecuzione del comando `npx n8n`).

### Setup Locale

```bash
cd src/app
npm install
npx n8n
```

Apri l'interfaccia: [http://localhost:5678](http://localhost:5678)

### Variabili d'Ambiente Principali

| Variabile | Scopo |
|-----------|-------|
| `N8N_BASIC_AUTH_ACTIVE` | Abilita Basic Auth (`true`/`false`) |
| `N8N_BASIC_AUTH_USER` | Username Basic Auth |
| `N8N_BASIC_AUTH_PASSWORD` | Password Basic Auth (cambiarla!) |
| `N8N_ENCRYPTION_KEY` | Chiave cifratura dati (impostare stabile) |
| `DB_TYPE` | Tipo DB (`sqlite`, `postgresdb`, `mysqldb`) |
| `GENERIC_TIMEZONE` | Timezone esecuzione workflows |

Imposta valori sicuri tramite secret manager / configurazione Databricks.

### Persistenza

SQLite va bene per test; per produzione usare Postgres o MySQL impostando le variabili di connessione richieste da n8n.

### Sicurezza

- Cambia sempre la password di default.
- Mantieni una chiave di cifratura stabile (`N8N_ENCRYPTION_KEY`).
- Limita l'accesso diretto alla porta 5678 se necessario, usando rete privata / regole di accesso.

### Aggiornamenti

Aggiorna la versione in `src/app/package.json`, esegui `npm install` e ridistribuisci.


