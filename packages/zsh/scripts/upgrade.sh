#!/usr/bin/env zsh
# custom script
printf "\n${BLUE}%s${RESET}\n" "Updating custom plugins and themes"
cd custom || { echo "Failed to change directory"; exit 1; }

for plugin in plugins/*/ themes/*/; do
  if [ -d "$plugin/.git" ]; then
    printf "${YELLOW}%s${RESET}\n" "${plugin%/}"
    git -C "$plugin" pull || { echo "Failed to pull changes"; exit 1; }
  fi
done