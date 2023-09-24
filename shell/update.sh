#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"
ZSH_DIR="$BASEDIR/zsh"
OH_MY_ZSH_DIR="$BASEDIR/oh-my-zsh"

cp ~/.zshrc "$ZSH_DIR"
cp -r ~/.oh-my-zsh/custom "$OH_MY_ZSH_DIR"
