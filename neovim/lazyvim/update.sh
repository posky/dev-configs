#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
rm -r "$BASEDIR/lua"
cp -r ~/.config/nvim/lua "$BASEDIR"
