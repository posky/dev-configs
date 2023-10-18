return {
  "nvimtools/none-ls.nvim",
  opts = function()
    local nls = require("null-ls")
    return {
      root_dir = require("null-ls.utils").root_pattern(".null-ls-root", ".neoconf.json", "Makefile", ".git"),
      sources = {
        -- nls.builtins.formatting.fish_indent,
        -- nls.builtins.diagnostics.fish,
        nls.builtins.formatting.stylua,
        nls.builtins.formatting.shfmt,
        -- nls.builtins.diagnostics.flake8,
        nls.builtins.formatting.prettierd,
        nls.builtins.diagnostics.buf,
        nls.builtins.formatting.buf,
        nls.builtins.diagnostics.npm_groovy_lint,
        -- nls.builtins.formatting.npm_groovy_lint,
      },
    }
  end,
}
