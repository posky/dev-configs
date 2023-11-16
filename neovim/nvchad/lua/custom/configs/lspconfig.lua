local configs = require "plugins.configs.lspconfig"
local on_attach = configs.on_attach
local capabilities = configs.capabilities
local nlspsettings = require "nlspsettings"

nlspsettings.setup {
  config_home = vim.fn.stdpath "config" .. "/nlsp-settings",
  local_settings_dir = ".nlsp-settings",
  local_settings_root_markers_fallback = { ".git" },
  append_default_schemas = true,
  loader = "json",
}

local lspconfig = require "lspconfig"
local servers = { "html", "cssls", "clangd", "pyright", "ruff_lsp", "taplo", "jsonls", "bufls" }

for _, lsp in ipairs(servers) do
  lspconfig[lsp].setup {
    on_attach = on_attach,
    capabilities = capabilities,
  }
end

lspconfig["groovyls"].setup {
  on_attach = on_attach,
  capabilities = capabilities,
  cmd = {
    "java",
    "-jar",
    os.getenv "HOME"
      .. "/.local/share/nvim/mason/packages/groovy-language-server/build/libs/groovy-language-server-all.jar",
  },
}
