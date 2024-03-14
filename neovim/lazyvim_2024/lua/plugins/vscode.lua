if not vim.g.vscode then
  return {}
end

local keymap = vim.keymap
local vscode = require("vscode-neovim")

keymap.set({ "n", "v" }, "gD", function()
  vscode.action("editor.action.revealDefinitionAside", {})
end)
keymap.set({ "n", "v" }, "gi", function()
  vscode.action("editor.action.goToImplementation", {})
end)
keymap.set({ "n", "v" }, "gr", function()
  vscode.action("editor.action.goToReferences", {})
end)
keymap.set({ "n", "v" }, "<leader>cr", function()
  vscode.action("editor.action.rename", {})
end)
keymap.set({ "n", "v" }, "<leader>ca", function()
  vscode.action("editor.action.quickFix", {})
end)

keymap.set("n", "]d", function()
  vscode.call("editor.action.marker.next")
end)
keymap.set("n", "[d", function()
  vscode.call("editor.action.marker.prev")
end)
