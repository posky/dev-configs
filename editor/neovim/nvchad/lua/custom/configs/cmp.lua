local cmp_sources = require("plugins.configs.cmp").sources

local opts = {
  sources = vim.list_extend(cmp_sources, { { name = "crates" } }),
}

return opts
