local opts = {
  ensure_installed = {
    "lua-language-server",
    "stylua",

    "css-lsp",
    "html-lsp",
    "typescript-language-server",
    "deno",
    "prettier",

    "shellcheck",

    "clangd",
    "clang-format",

    -- python
    "pyright",
    "ruff-lsp",
    "ruff",
    "black",

    -- rust
    "rust-analyzer",

    -- toml
    "taplo",

    -- groovy
    "groovy-language-server",

    -- jsonls
    "json-lsp",
    "jsonlint",

    -- protobufs
    "buf-language-server",
    "protolint",
    "buf",
  },
}

return opts
