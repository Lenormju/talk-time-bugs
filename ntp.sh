#!/usr/bin/env bash
# Lance le serveur local de la démo NTP (slide « Démo : interroger un serveur NTP »).
# Options passées au script : --port N, --no-udp
set -euo pipefail
cd "$(dirname "$0")"
exec uv run scripts/ntp_server.py "$@"
