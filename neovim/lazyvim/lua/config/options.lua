-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here
local opt = vim.opt
local g = vim.g
local ft = vim.filetype

opt.wrap = true

g.autoformat = true

-- set filetype
ft.add({
  filename = {
    ["Jenkinsfile"] = "groovy",
  },
})
