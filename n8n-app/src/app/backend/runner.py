import os
import signal
import subprocess
import sys
import threading
import time

"""Runner that starts n8n (Node.js) and the FastAPI app (uvicorn) in the same Databricks App process.

This approach lets Databricks Apps run both services side by side. n8n will listen on port 5678
by default; FastAPI will listen on port 8000. You can expose/route externally via Databricks App
ingress rules (configure separately if needed) or use FastAPI as a lightweight proxy.

Environment variables you can set via Databricks (or here as defaults):
  N8N_BASIC_AUTH_ACTIVE=true
  N8N_BASIC_AUTH_USER=admin
  N8N_BASIC_AUTH_PASSWORD=changeme
  N8N_ENCRYPTION_KEY=<provide-32+ chars>
  DB_TYPE=sqlite   (default)
  GENERIC_TIMEZONE=Europe/Rome

IMPORTANT: For production do not use the default basic auth password.
"""


def ensure_env_defaults():
    os.environ.setdefault("DB_TYPE", "sqlite")
    os.environ.setdefault("N8N_BASIC_AUTH_ACTIVE", "true")
    os.environ.setdefault("N8N_BASIC_AUTH_USER", "admin")
    os.environ.setdefault("N8N_BASIC_AUTH_PASSWORD", "admin")  # CHANGE in production
    if "N8N_ENCRYPTION_KEY" not in os.environ:
        # Simple generated key; replace with a secure secret manager retrieval.
        os.environ["N8N_ENCRYPTION_KEY"] = os.urandom(32).hex()
    os.environ.setdefault("GENERIC_TIMEZONE", "Europe/Rome")


def start_n8n():
    # Use npx to ensure local dependency resolution.
    cmd = ["npx", "n8n"]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def stream_output(proc, prefix):
    for line in proc.stdout:
        print(f"[{prefix}] {line}", end="", flush=True)


def start_uvicorn():
    cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def main():
    ensure_env_defaults()
    print("Starting n8n and FastAPI (uvicorn)...", flush=True)

    n8n_proc = start_n8n()
    api_proc = start_uvicorn()

    # Output threads
    t1 = threading.Thread(target=stream_output, args=(n8n_proc, "n8n"), daemon=True)
    t2 = threading.Thread(target=stream_output, args=(api_proc, "api"), daemon=True)
    t1.start(); t2.start()

    # Graceful shutdown handling
    shutdown = threading.Event()

    def handle_signal(signum, frame):
        print(f"Received signal {signum}, shutting down...", flush=True)
        shutdown.set()
        for p in (n8n_proc, api_proc):
            if p.poll() is None:
                try:
                    p.terminate()
                except Exception:
                    pass

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Monitor processes
    try:
        while not shutdown.is_set():
            if n8n_proc.poll() is not None:
                print("n8n process exited; terminating api", flush=True)
                shutdown.set()
            if api_proc.poll() is not None:
                print("API process exited; terminating n8n", flush=True)
                shutdown.set()
            time.sleep(2)
    finally:
        for p in (n8n_proc, api_proc):
            if p.poll() is None:
                try:
                    p.terminate()
                except Exception:
                    pass
        print("Shutdown complete", flush=True)


if __name__ == "__main__":
    main()
