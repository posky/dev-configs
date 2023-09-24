#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
echo $BASEDIR
cp -r ~/.hammerspoon "$BASEDIR"