#!/usr/bin/env -S nvim -l
-- called by scripts/update.sh
-- refer .github/workflows/update.yml
---@diagnostic disable: undefined-global
-- add nvim-treesitter to path
vim.o.runtimepath = vim.o.runtimepath .. ",nvim-treesitter"
print(vim.fn.json_encode(require "nvim-treesitter.parsers".get_parser_configs()))
