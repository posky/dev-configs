#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
cp "$BASEDIR/.wezterm.lua" ~/
cp "$BASEDIR/config" ~/.config/ghostty/
