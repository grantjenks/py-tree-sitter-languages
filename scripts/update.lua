#!/usr/bin/env -S nvim -l
-- this script relies on the parser configuration used by the nvim-treesitter
-- repository (https://github.com/nvim-treesitter/nvim-treesitter) to update the
-- various parsers built in py-tree-sitter-languages
--
-- called by scripts/update.sh
-- refer .github/workflows/update.yml
---@diagnostic disable: undefined-global
local path = "nvim-treesitter"
if #vim.v.argv > 3 then
    path = vim.v.argv[4]
end
-- add nvim-treesitter to path
vim.o.runtimepath = vim.o.runtimepath .. "," .. path
vim.print(vim.fn.json_encode(require "nvim-treesitter.parsers".get_parser_configs()))
