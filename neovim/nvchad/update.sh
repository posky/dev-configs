#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")/lua"
rm -r "$BASEDIR/custom"
cp -r ~/.config/nvim/lua/custom "$BASEDIR"
