#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/.config/zed/settings.json"

if [ -f "$SETTING_PATH" ]; then
  echo "Updating Zed setting"
  cp "$BASEDIR/settings.json" "$SETTING_PATH"
fi
