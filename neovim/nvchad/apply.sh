#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")/lua"
rm -rf ~/.config/nvim/lua/custom
cp -r "$BASEDIR" ~/.config/nvim
