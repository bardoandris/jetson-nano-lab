#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv-jetson"
PKG_FILE="$SCRIPT_DIR/pip-pkgs.txt"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
if [ -f "$PKG_FILE" ]; then
  "$VENV_DIR/bin/python" -m pip install -r "$PKG_FILE"
else
  echo "Warning: $PKG_FILE not found; skipping package installation." >&2
fi
