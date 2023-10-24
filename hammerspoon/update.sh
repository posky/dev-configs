#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
rm -r "$BASEDIR/.hammerspoon"
cp -r ~/.hammerspoon "$BASEDIR"
