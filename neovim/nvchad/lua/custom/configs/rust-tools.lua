local opts = {
  tools = { -- rust-tools options

    -- how to execute terminal commands
    -- options right now: termopen / quickfix / toggleterm / vimux
    -- executor = require("rust-tools.executors").termopen,

    -- callback to execute once rust-analyzer is done initializing the workspace
    -- The callback receives one parameter indicating the `health` of the server: "ok" | "warning" | "error"
    on_initialized = nil,

    -- automatically call RustReloadWorkspace when writing to a Cargo.toml file.
    reload_workspace_from_cargo_toml = true,

    -- These apply to the default RustSetInlayHints command
    inlay_hints = {
      -- automatically set inlay hints (type hints)
      -- default: true
      auto = true,

      -- Only show inlay hints for the current line
      only_current_line = false,

      -- whether to show parameter hints with the inlay hints or not
      -- default: true
      show_parameter_hints = true,

      -- prefix for parameter hints
      -- default: "<-"
      parameter_hints_prefix = "<- ",

      -- prefix for all the other hints (type, chaining)
      -- default: "=>"
      other_hints_prefix = "=> ",

      -- whether to align to the length of the longest line in the file
      max_len_align = false,

      -- padding from the left if max_len_align is true
      max_len_align_padding = 1,

      -- whether to align to the extreme right or not
      right_align = false,

      -- padding from the right if right_align is true
      right_align_padding = 7,

      -- The color of the hints
      highlight = "Comment",
    },

    -- options same as lsp hover / vim.lsp.util.open_floating_preview()
    hover_actions = {

      -- the border that is used for the hover window
      -- see vim.api.nvim_open_win()
      border = {
        { "╭", "FloatBorder" },
        { "─", "FloatBorder" },
        { "╮", "FloatBorder" },
        { "│", "FloatBorder" },
        { "╯", "FloatBorder" },
        { "─", "FloatBorder" },
        { "╰", "FloatBorder" },
        { "│", "FloatBorder" },
      },

      -- Maximal width of the hover window. Nil means no max.
      max_width = nil,

      -- Maximal height of the hover window. Nil means no max.
      max_height = nil,

      -- whether the hover action window gets automatically focused
      -- default: false
      auto_focus = false,
    },

    -- settings for showing the crate graph based on graphviz and the dot
    -- command
    crate_graph = {
      -- Backend used for displaying the graph
      -- see: https://graphviz.org/docs/outputs/
      -- default: x11
      backend = "x11",
      -- where to store the output, nil for no output stored (relative
      -- path from pwd)
      -- default: nil
      output = nil,
      -- true for all crates.io and external crates, false only the local
      -- crates
      -- default: true
      full = true,

      -- List of backends found on: https://graphviz.org/docs/outputs/
      -- Is used for input validation and autocompletion
      -- Last updated: 2021-08-26
      enabled_graphviz_backends = {
        "bmp",
        "cgimage",
        "canon",
        "dot",
        "gv",
        "xdot",
        "xdot1.2",
        "xdot1.4",
        "eps",
        "exr",
        "fig",
        "gd",
        "gd2",
        "gif",
        "gtk",
        "ico",
        "cmap",
        "ismap",
        "imap",
        "cmapx",
        "imap_np",
        "cmapx_np",
        "jpg",
        "jpeg",
        "jpe",
        "jp2",
        "json",
        "json0",
        "dot_json",
        "xdot_json",
        "pdf",
        "pic",
        "pct",
        "pict",
        "plain",
        "plain-ext",
        "png",
        "pov",
        "ps",
        "ps2",
        "psd",
        "sgi",
        "svg",
        "svgz",
        "tga",
        "tiff",
        "tif",
        "tk",
        "vml",
        "vmlz",
        "wbmp",
        "webp",
        "xlib",
        "x11",
      },
    },
  },

  -- all the opts to send to nvim-lspconfig
  -- these override the defaults set by rust-tools.nvim
  -- see https://github.com/neovim/nvim-lspconfig/blob/master/doc/server_configurations.md#rust_analyzer
  server = {
    on_attach = function(_, bufnr)
      require("core.utils").load_mappings("lspconfig", { buffer = bufnr })
    end,
    capabilities = {
      experimental = {
        serverStatusNotification = true,
      },
      general = {
        positionEncodings = { "utf-16" },
      },
      textDocument = {
        callHierarchy = {
          dynamicRegistration = false,
        },
        codeAction = {
          codeActionLiteralSupport = {
            codeActionKind = {
              valueSet = {
                "",
                "quickfix",
                "refactor",
                "refactor.extract",
                "refactor.inline",
                "refactor.rewrite",
                "source",
                "source.organizeImports",
              },
            },
          },
          dataSupport = true,
          dynamicRegistration = true,
          isPreferredSupport = true,
          resolveSupport = {
            properties = { "edit" },
          },
        },
        completion = {
          completionItem = {
            commitCharactersSupport = false,
            deprecatedSupport = false,
            documentationFormat = { "markdown", "plaintext" },
            preselectSupport = false,
            snippetSupport = false,
          },
          completionItemKind = {
            valueSet = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 },
          },
          contextSupport = false,
          dynamicRegistration = false,
        },
        declaration = {
          linkSupport = true,
        },
        definition = {
          dynamicRegistration = true,
          linkSupport = true,
        },
        diagnostic = {
          dynamicRegistration = false,
        },
        documentHighlight = {
          dynamicRegistration = false,
        },
        documentSymbol = {
          dynamicRegistration = false,
          hierarchicalDocumentSymbolSupport = true,
          symbolKind = {
            valueSet = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26 },
          },
        },
        formatting = {
          dynamicRegistration = true,
        },
        hover = {
          contentFormat = { "markdown", "plaintext" },
          dynamicRegistration = true,
        },
        implementation = {
          linkSupport = true,
        },
        inlayHint = {
          dynamicRegistration = true,
          resolveSupport = {
            properties = {},
          },
        },
        publishDiagnostics = {
          dataSupport = true,
          relatedInformation = true,
          tagSupport = {
            valueSet = { 1, 2 },
          },
        },
        rangeFormatting = {
          dynamicRegistration = true,
        },
        references = {
          dynamicRegistration = false,
        },
        rename = {
          dynamicRegistration = true,
          prepareSupport = true,
        },
        semanticTokens = {
          augmentsSyntaxTokens = true,
          dynamicRegistration = false,
          formats = { "relative" },
          multilineTokenSupport = false,
          overlappingTokenSupport = true,
          requests = {
            full = {
              delta = true,
            },
            range = false,
          },
          serverCancelSupport = false,
          tokenModifiers = {
            "declaration",
            "definition",
            "readonly",
            "static",
            "deprecated",
            "abstract",
            "async",
            "modification",
            "documentation",
            "defaultLibrary",
          },
          tokenTypes = {
            "namespace",
            "type",
            "class",
            "enum",
            "interface",
            "struct",
            "typeParameter",
            "parameter",
            "variable",
            "property",
            "enumMember",
            "event",
            "function",
            "method",
            "macro",
            "keyword",
            "modifier",
            "comment",
            "string",
            "number",
            "regexp",
            "operator",
            "decorator",
          },
        },
        signatureHelp = {
          dynamicRegistration = false,
          signatureInformation = {
            activeParameterSupport = true,
            documentationFormat = { "markdown", "plaintext" },
            parameterInformation = {
              labelOffsetSupport = true,
            },
          },
        },
        synchronization = {
          didSave = true,
          dynamicRegistration = false,
          willSave = true,
          willSaveWaitUntil = true,
        },
        typeDefinition = {
          linkSupport = true,
        },
      },
      window = {
        showDocument = {
          support = true,
        },
        showMessage = {
          messageActionItem = {
            additionalPropertiesSupport = false,
          },
        },
        workDoneProgress = true,
      },
      workspace = {
        applyEdit = true,
        configuration = true,
        didChangeWatchedFiles = {
          dynamicRegistration = true,
          relativePatternSupport = true,
        },
        inlayHint = {
          refreshSupport = true,
        },
        semanticTokens = {
          refreshSupport = true,
        },
        symbol = {
          dynamicRegistration = false,
          symbolKind = {
            valueSet = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26 },
          },
        },
        workspaceEdit = {
          resourceOperations = { "rename", "create", "delete" },
        },
        workspaceFolders = true,
      },
    },
    -- standalone file support
    -- setting it to false may improve startup time
    standalone = true,
    settings = {
      ["rust-anlyzer"] = {
        cargo = {
          autoreload = true,
          buildScripts = { enable = true },
          features = { "all" },
        },
        checkOnSave = true,
        check = {
          command = "clippy",
        },
        inlayHints = {
          bindingModeHints = { enable = true },
          closureCaptureHints = { enable = true },
        },
        procMacro = {
          enable = true,
        },
        rustfmt = {
          extraArgs = { "+nightly" },
        },
      },
    },
  }, -- rust-analyzer options

  -- debugging stuff
  -- dap = {
  --   adapter = {
  --     type = "executable",
  --     command = "lldb-vscode",
  --     name = "rt_lldb",
  --   },
  -- },
}

require("rust-tools").setup(opts)
