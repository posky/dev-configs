#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$(lazygit -cd)/config.yml"

if [ -f "$SETTING_PATH" ]; then
  echo "Updating lazygit setting"
  cp "$BASEDIR/config.yml" "$SETTING_PATH"
fi
