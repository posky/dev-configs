#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/.config/zed/settings.json"

if [ -f "$SETTING_PATH" ]; then
  echo "Diff Zed setting"
  code --diff "$BASEDIR/settings.json" "$SETTING_PATH"
fi
