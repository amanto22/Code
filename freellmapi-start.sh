#!/usr/bin/env bash
# Avvio di FreeLLMAPI su macOS.
# Prima esecuzione: clona il repo, installa le dipendenze, crea .env con chiave di cifratura.
# Esecuzioni successive: aggiorna il codice e avvia il server.
# Uso: bash freellmapi-start.sh [--no-update]

set -euo pipefail

REPO_URL="https://github.com/tashfeenahmed/freellmapi.git"
INSTALL_DIR="${FREELLMAPI_DIR:-$HOME/freellmapi}"
PORT="${FREELLMAPI_PORT:-3001}"
UPDATE=1
[[ "${1:-}" == "--no-update" ]] && UPDATE=0

err() { echo "Errore: $*" >&2; exit 1; }

# Prerequisiti
command -v git >/dev/null     || err "git non trovato. Installa con: xcode-select --install"
command -v openssl >/dev/null || err "openssl non trovato."
command -v node >/dev/null    || err "Node.js non trovato. Installa con: brew install node"
command -v npm >/dev/null     || err "npm non trovato."

NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
[[ "$NODE_MAJOR" -ge 20 ]] || err "Serve Node.js 20 o superiore (trovato $(node -v)). Aggiorna con: brew upgrade node"

# Clone o aggiornamento
if [[ ! -d "$INSTALL_DIR/.git" ]]; then
  echo "Clono FreeLLMAPI in $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
  FIRST_RUN=1
else
  FIRST_RUN=0
  if [[ "$UPDATE" -eq 1 ]]; then
    echo "Aggiorno il codice"
    git -C "$INSTALL_DIR" pull --ff-only || echo "Aggiornamento saltato (modifiche locali o rete)."
  fi
fi

cd "$INSTALL_DIR"

# Dipendenze: solo se prima esecuzione, aggiornamento avvenuto o node_modules assente
if [[ "$FIRST_RUN" -eq 1 || "$UPDATE" -eq 1 || ! -d node_modules ]]; then
  echo "Installo le dipendenze"
  npm install
fi

# .env: creato una volta sola. La chiave di cifratura non va mai rigenerata,
# altrimenti le chiavi provider gia salvate non sono piu leggibili.
if [[ ! -f .env ]]; then
  [[ -f .env.example ]] && cp .env.example .env || touch .env
fi
if ! grep -q '^ENCRYPTION_KEY=' .env; then
  printf '\nENCRYPTION_KEY=%s\n' "$(openssl rand -hex 32)" >> .env
  echo "Chiave di cifratura generata in $INSTALL_DIR/.env (fanne un backup)."
fi
if ! grep -q '^PORT=' .env; then
  printf 'PORT=%s\n' "$PORT" >> .env
fi
chmod 600 .env

# Porta occupata?
if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  err "La porta $PORT e gia in uso. Cambia con: FREELLMAPI_PORT=3002 bash $0"
fi

# Apre il browser appena il server risponde
( for _ in $(seq 1 60); do
    if curl -s -o /dev/null "http://localhost:$PORT"; then open "http://localhost:$PORT"; break; fi
    sleep 1
  done ) &

echo "Avvio su http://localhost:$PORT (CTRL+C per fermare)"
exec npm run dev
