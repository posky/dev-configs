local opts = {
  ensure_installed = {
    -- defaults
    "vim",
    "lua",

    -- web dev
    "html",
    "css",
    "javascript",
    "typescript",
    "tsx",
    "json",

    -- low level
    "c",
    "zig",

    "markdown",
    "markdown_inline",

    "rst",

    -- python
    "python",
    "ninja",

    -- rust
    "ron",
    "rust",
    "toml",

    -- groovy
    "groovy",
  },
  indent = {
    enable = true,
    disable = { "rust" },
  },
}

return opts
