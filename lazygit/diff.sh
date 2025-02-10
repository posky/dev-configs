#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$(lazygit -cd)/config.yml"

if [ -f "$SETTING_PATH" ]; then
  echo "Diff lazygit setting"
  if command -v code >/dev/null 2>&1; then
    code --diff "$BASEDIR/config.yml" "$SETTING_PATH"
  else
    vim -d "$BASEDIR/config.yml" "$SETTING_PATH"
  fi
fi
