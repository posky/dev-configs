#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")/lua"
cp -r ~/.config/nvim/lua/custom "$BASEDIR"
