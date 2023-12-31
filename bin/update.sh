#!/bin/sh
BASEDIR="$(dirname "$(realpath "$0")")"

# git
if [ -f "$HOME/.gitmessage.txt" ]; then
	echo "Updating git..."
	sh "$BASEDIR/../git/update.sh"
fi

# hammerspoon
if [ -d "$HOME/.hammerspoon" ]; then
	echo "Updating hammerspoon..."
	sh "$BASEDIR/../hammerspoon/update.sh"
else
	echo "Not found hammerspoon"
fi

# neovim - lazyvim
if [ -f "$HOME/.config/nvim/lua/config/lazy.lua" ]; then
	echo "Updating neovim - lazyvim..."
	sh "$BASEDIR/../neovim/lazyvim/update.sh"
else
	echo "Not found neovim - lazyvim"
fi

# neovim - nvchad
if [ -f "$HOME/.config/nvim/lua/custom/chadrc.lua" ]; then
	echo "Updating neovim - nvchad..."
	sh "$BASEDIR/../neovim/nvchad/update.sh"
else
	echo "Not found neovim - nvchad"
fi

# shell
if [ -f "$HOME/.zshrc" ]; then
	echo "Updating zsh..."
	sh "$BASEDIR/../shell/update.sh"
else
	echo "Not found zsh"
fi

# terminal - kitty
if [ -d "$HOME/.config/kitty" ]; then
	echo "Updating kitty..."
	sh "$BASEDIR/../terminal/kitty/update.sh"
else
	echo "Not found kitty"
fi

# terminal - wezterm
if [ -f "$HOME/.wezterm.lua" ]; then
  echo "Updating wezterm..."
  sh "$BASEDIR/../terminal/wezterm/update.sh"
else
  echo "Not found wezterm"
fi

# vscode
if [ -f "$HOME/Library/Application Support/Code/User/keybindings.json" ]; then
	echo "Updating vscode..."
	sh "$BASEDIR/../vscode/macos/update.sh"
else
	echo "Not found vscode"
fi
