#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/Library/Application Support/Windsurf/User/settings.json"

echo "$BASEDIR"

if [ -f "$SETTING_PATH" ]; then
  echo "Updating Windsurf setting"
  cp "$SETTING_PATH" "$BASEDIR"
fi
