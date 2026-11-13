#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_SRC="$ROOT/skills/investment-intelligence"
SKILL_DIR="$HOME/.hermes/skills"
TARGET="$SKILL_DIR/investment-intelligence"
mkdir -p "$SKILL_DIR"
if [[ -e "$TARGET" && ! -L "$TARGET" ]]; then
  BACKUP="$TARGET.backup.$(date +%Y%m%d%H%M%S)"
  mv "$TARGET" "$BACKUP"
  echo "Existing skill moved to: $BACKUP"
elif [[ -L "$TARGET" ]]; then
  rm "$TARGET"
fi
ln -s "$SKILL_SRC" "$TARGET"
test -f "$TARGET/SKILL.md"
echo "Installed Hermes skill: $TARGET"
echo "Source: $SKILL_SRC"
echo "No packages or API keys were installed."
