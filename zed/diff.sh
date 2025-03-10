#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/.config/zed/settings.json"

if [ -f "$SETTING_PATH" ]; then
  echo "Diff Zed setting"
  if command -v code > /dev/null 2>&1; then
    code --diff "$BASEDIR/settings.json" "$SETTING_PATH"
  else
    vim -d "$BASEDIR/settings.json" "$SETTING_PATH"
  fi 
fi
