#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/Library/Application Support/Windsurf/User/settings.json"

cp "$BASEDIR/settings.json" "$SETTING_PATH"
