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

# One-shot recovery hatch: set FORCE_REINSTALL=1 in the Render env to WIPE and
# recreate the schema on next boot. This re-runs listmonk's full --install, which
# recreates the super admin from LISTMONK_ADMIN_USER / LISTMONK_ADMIN_PASSWORD.
# Use only on an empty/disposable DB (destroys all data). Set it back to 0 after.
# Rationale: LISTMONK_ADMIN_PASSWORD only sets the admin password at first install;
# changing it later does nothing to an already-created admin, so a mis-set password
# can strand you out. This lets us reset without external DB access.
if [ "${FORCE_REINSTALL}" = "1" ]; then
  echo "==> FORCE_REINSTALL=1 : wiping and reinstalling schema (recreates admin from env)"
  ./listmonk --install --yes --config ''
else
  ./listmonk --install --idempotent --yes --config ''
fi
./listmonk --upgrade --yes --config ''

exec ./listmonk --config ''
