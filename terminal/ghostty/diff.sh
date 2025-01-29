#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
LOCAL_PATH="$BASEDIR/config"
SETTING_PATH="$HOME/.config/ghostty/config"

if [ -f "$SETTING_PATH" ]; then
  echo "Diff Ghostty setting"
  if command -v code >/dev/null 2>&1; then
    code --diff "$LOCAL_PATH" "$SETTING_PATH"
  else
    vim -d "$LOCAL_PATH" "$SETTING_PATH"
  fi
fi
