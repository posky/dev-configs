local null_ls = require "null-ls"

local opts = {
  src = {
    cmp = {
      enabled = true,
    },
  },
  null_ls = {
    enabled = true,
    name = "crates.nvim",
  },
}

require("crates").setup(opts)
