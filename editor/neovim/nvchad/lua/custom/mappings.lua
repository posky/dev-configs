local M = {}

M.general = {
  n = {
    [";"] = { ":", "enter command mode", opts = { nowait = true } },
  },
}

M.lspconfig = {
  n = {
    ["gd"] = {
      function()
        require("telescope.builtin").lsp_definitions()
      end,
      "LSP definition",
    },

    ["gi"] = {
      function()
        require("telescope.builtin").lsp_implementations()
      end,
      "LSP implementation",
    },

    ["<leader>D"] = {
      function()
        require("telescope.builtin").lsp_type_definitions()
      end,
      "LSP definition type",
    },

    ["gr"] = {
      function()
        require("telescope.builtin").lsp_references()
      end,
      "LSP references",
    },

    ["<leader>q"] = {
      function()
        require("telescope.builtin").diagnostics()
      end,
      "Diagnostic setloclist",
    },

    ["<leader>ss"] = {
      function()
        require("telescope.builtin").lsp_document_symbols()
      end,
      "Document symbols",
    },
  },
}

M.nvterm = {
  t = {
    -- toggle in terminal mode
    ["<C-;>"] = {
      function()
        require("nvterm.terminal").toggle "float"
      end,
      "Toggle floating term",
    },
  },

  n = {
    -- toggle in normal mode
    ["<C-;>"] = {
      function()
        require("nvterm.terminal").toggle "float"
      end,
      "Toggle floating term",
    },
  },
}

return M
