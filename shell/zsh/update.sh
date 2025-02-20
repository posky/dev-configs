#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
SETTING_PATH="$HOME/.zshrc"

if [ -f "$SETTING_PATH" ]; then
  echo "Updating Zsh setting"
  cp "$SETTING_PATH" "$BASEDIR"
fi
