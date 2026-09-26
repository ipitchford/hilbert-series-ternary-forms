#!/usr/bin/env bash
# Usage: PY=/path/to/python ./replay.sh [archived|fresh|full]
#   archived (default, about 1 min): all certificates and checks on the archived data; no coefficient regenerated.
#   fresh    (about 3 min): adds bounded fresh recomputation (blind torus program, validation grids, septic to 120, spot checks).
#   full     (about 2.5 h): adds full regeneration of every archived coefficient file, byte-compared with the archive.
# Needs python-flint and sympy, and a C compiler with OpenMP (set CC to choose one). See scripts/replay.py.
set -euo pipefail
cd "$(dirname "$0")"
exec "${PY:-python3}" scripts/replay.py "${1:-archived}"
