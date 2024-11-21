#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/Library/Application Support/Windsurf/User/settings.json"

if [ -f "$SETTING_PATH" ]; then
  echo "Updating Windsurf setting"
  cp "$BASEDIR/settings.json" "$SETTING_PATH"
fi
