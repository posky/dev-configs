local autocmd = vim.api.nvim_create_autocmd
local opt = vim.opt
local g = vim.g
local api = vim.api
local cmd = vim.cmd
local ft = vim.filetype

-- NOTE: rustfmt
-- rust.vim
g.rustfmt_command = "rustfmt +nightly"
g.rustfmt_autosave = 1

-- groovy
ft.add { filename = { ["Jenkinsfile"] = "groovy" } }
autocmd("BufWritePost", {
  pattern = "Jenkinsfile",
  callback = function(event)
    vim.cmd("!npm-groovy-lint --format " .. event.file)
  end,
})
