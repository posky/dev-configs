#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/.zshrc"

if [ -f "$SETTING_PATH" ]; then
  echo "Diff zsh setting"
  if command -v code >/dev/null 2>&1; then
    code --diff "$BASEDIR/.zshrc" "$SETTING_PATH"
  else
    vim -d "$BASEDIR/.zshrc" "$SETTING_PATH"
  fi
fi
