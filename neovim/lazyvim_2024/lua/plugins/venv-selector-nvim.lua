return {
  "linux-cultist/venv-selector.nvim",
  opts = function(_, opts)
    if type(opts.name) == "table" then
      vim.list_extend(opts.name, { ".hatch" })
    end
  end,
}
