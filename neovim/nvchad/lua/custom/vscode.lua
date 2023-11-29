local opt = vim.opt
local vscode = require "vscode-neovim"

opt.ignorecase = true
opt.smartcase = true

-- keybindings
vim.g.mapleader = " "
vim.keymap.set("n", ";", ":", { noremap = true })
vim.keymap.set({ "n", "v" }, "gd", function()
  vscode.action("editor.action.revealDefinition", {})
end)
vim.keymap.set({ "n", "v" }, "gD", function()
  vscode.action("editor.action.revealDefinitionAside", {})
end)
vim.keymap.set({ "n", "v" }, "gi", function()
  vscode.action("editor.action.goToImplementation", {})
end)
vim.keymap.set({ "n", "v" }, "gr", function()
  vscode.action("editor.action.goToReferences", {})
end)
vim.keymap.set({ "n", "v" }, "<leader>ra", function()
  vscode.action("editor.action.rename", {})
end)
vim.keymap.set({ "n", "v" }, "<leader>ca", function()
  vscode.action("editor.action.quickFix", {})
end)
vim.keymap.set({ "n", "v" }, "K", function()
  vscode.action("editor.action.showDefinitionPreviewHover", {})
end)
vim.keymap.set("n", "<leader>ss", function()
  vscode.action("workbench.action.gotoSymbol", {})
end)

vim.keymap.set("n", "]d", function()
  vscode.call "editor.action.marker.next"
end)
vim.keymap.set("n", "[d", function()
  vscode.call "editor.action.marker.prev"
end)
vim.keymap.set("n", "<leader>ff", function()
  vscode.call "workbench.action.quickOpen"
end)
vim.keymap.set("n", "<leader>fw", function()
  vscode.call "workbench.action.findInFiles"
end)
vim.keymap.set({ "n", "v" }, "<leader>/", function()
  vscode.call "editor.action.commentLine"
end)
vim.keymap.set("n", "<leader>x", function()
  vscode.call "workbench.action.closeActiveEditor"
end)
