local opts = {
  terminals = {
    type_opts = {
      float = {
        row = 0.2,
        col = 0.1,
        width = 0.8,
        height = 0.6,
      },
    },
  },
}

require("nvterm").setup(opts)
