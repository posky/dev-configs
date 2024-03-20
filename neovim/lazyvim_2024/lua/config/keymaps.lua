-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
if vim.g.vscode then
  local keymap = vim.keymap
  local vscode = require("vscode-neovim")

  -- LSP
  keymap.set({ "n", "v" }, "gD", function()
    vscode.action("editor.action.revealDefinitionAside", {})
  end)
  keymap.set({ "n", "v" }, "gi", function()
    vscode.action("editor.action.goToImplementation", {})
  end)
  keymap.set({ "n", "v" }, "gr", function()
    vscode.action("editor.action.goToReferences", {})
  end)
  keymap.set({ "n", "v" }, "gy", function()
    vscode.action("editor.action.goToTypeDefinition", {})
  end)
  keymap.set({ "n" }, "gK", function()
    vscode.action("editor.action.triggerParameterHints", {})
  end)
  keymap.set({ "i" }, "<C-k>", function()
    vscode.action("editor.action.triggerParameterHints", {})
  end)
  keymap.set({ "n" }, "<leader>sS", function()
    vscode.action("workbench.action.showAllSymbols", {})
  end)
  keymap.set({ "n", "v" }, "<leader>cr", function()
    vscode.action("editor.action.rename", {})
  end)
  keymap.set({ "n", "v" }, "<leader>ca", function()
    vscode.action("editor.action.quickFix", {})
  end)

  keymap.set("n", "]d", function()
    vscode.action("editor.action.marker.nextInFiles", {})
  end)
  keymap.set("n", "[d", function()
    vscode.action("editor.action.marker.prevInFiles", {})
  end)
end
