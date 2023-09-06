local autocmd = vim.api.nvim_create_autocmd
local opt = vim.opt
local g = vim.g
local api = vim.api
local cmd = vim.cmd

-- NOTE: rustfmt
-- rust.vim
g.rustfmt_command = "rustfmt +nightly"
g.rustfmt_autosave = 1
