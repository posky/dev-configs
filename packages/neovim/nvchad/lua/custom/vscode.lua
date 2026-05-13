local opt = vim.opt
local g = vim.g
local keymap = vim.keymap
local vscode = require "vscode-neovim"

opt.ignorecase = true
opt.smartcase = true
opt.clipboard = "unnamedplus"

-- keybindings
g.mapleader = " "
keymap.set("n", ";", ":", { noremap = true })
keymap.set({ "n", "v" }, "gd", function()
  vscode.action("editor.action.revealDefinition", {})
end)
keymap.set({ "n", "v" }, "gD", function()
  vscode.action("editor.action.revealDefinitionAside", {})
end)
keymap.set({ "n", "v" }, "gi", function()
  vscode.action("editor.action.goToImplementation", {})
end)
keymap.set({ "n", "v" }, "gr", function()
  vscode.action("editor.action.goToReferences", {})
end)
keymap.set({ "n", "v" }, "<leader>ra", function()
  vscode.action("editor.action.rename", {})
end)
keymap.set({ "n", "v" }, "<leader>ca", function()
  vscode.action("editor.action.quickFix", {})
end)
keymap.set({ "n", "v" }, "K", function()
  vscode.action("editor.action.showDefinitionPreviewHover", {})
end)
keymap.set("n", "<leader>ss", function()
  vscode.action("workbench.action.gotoSymbol", {})
end)

keymap.set("n", "]d", function()
  vscode.call "editor.action.marker.next"
end)
keymap.set("n", "[d", function()
  vscode.call "editor.action.marker.prev"
end)
keymap.set("n", "<leader>ff", function()
  vscode.call "workbench.action.quickOpen"
end)
keymap.set("n", "<leader>fw", function()
  vscode.call "workbench.action.findInFiles"
end)
keymap.set({ "n", "v" }, "<leader>/", function()
  vscode.call "editor.action.commentLine"
end)
keymap.set("n", "<leader>x", function()
  vscode.call "workbench.action.closeActiveEditor"
end)

-- lazy
local lazypath = vim.fn.stdpath "data" .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system {
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  }
end
vim.opt.rtp:prepend(lazypath)

local plugins = {
  {
    "kylechui/nvim-surround",
    version = "*",
    event = "VeryLazy",
    config = function()
      require("nvim-surround").setup()
    end,
  },
}

local opts = {}

require("lazy").setup(plugins, opts)
