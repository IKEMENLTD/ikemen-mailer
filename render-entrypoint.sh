#!/bin/sh
# Render entrypoint for IKEMEN MAILER (listmonk fork).
# - Binds to Render's injected $PORT (falls back to 9000 for local runs).
# - `--config ''` makes listmonk ignore config.toml and read ONLY LISTMONK_* env vars
#   (DB creds etc. are set in the Railway service variables).
# - --install --idempotent : creates the schema only on a fresh DB (safe every boot).
# - --upgrade              : applies any pending migrations after an image update.
set -e

export LISTMONK_app__address="0.0.0.0:${PORT:-9000}"
echo "==> Starting IKEMEN MAILER on ${LISTMONK_app__address}"

./listmonk --install --idempotent --yes --config ''
./listmonk --upgrade --yes --config ''

exec ./listmonk --config ''
