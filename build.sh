pip install cython
pip install -e .

mkdir vendor
cd vendor

git clone --depth 1 https://github.com/AbstractMachinesLab/tree-sitter-erlang
git clone --depth 1 https://github.com/Azganoth/tree-sitter-lua
git clone --depth 1 https://github.com/Wilfred/tree-sitter-elisp
git clone --depth 1 https://github.com/alemuller/tree-sitter-make
git clone --depth 1 https://github.com/camdencheek/tree-sitter-dockerfile
git clone --depth 1 https://github.com/camdencheek/tree-sitter-go-mod
git clone --depth 1 https://github.com/elixir-lang/tree-sitter-elixir
git clone --depth 1 https://github.com/elm-tooling/tree-sitter-elm
git clone --depth 1 https://github.com/fwcd/tree-sitter-kotlin
git clone --depth 1 https://github.com/ganezdragon/tree-sitter-perl
git clone --depth 1 https://github.com/ikatyang/tree-sitter-markdown
git clone --depth 1 https://github.com/ikatyang/tree-sitter-toml
git clone --depth 1 https://github.com/ikatyang/tree-sitter-yaml
git clone --depth 1 https://github.com/jiyee/tree-sitter-objc
git clone --depth 1 https://github.com/m-novikov/tree-sitter-sql
git clone --depth 1 https://github.com/r-lib/tree-sitter-r
git clone --depth 1 https://github.com/rydesun/tree-sitter-dot
git clone --depth 1 https://github.com/slackhq/tree-sitter-hack
git clone --depth 1 https://github.com/theHamsta/tree-sitter-commonlisp
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-bash
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-c
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-c-sharp
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-cpp
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-css
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-embedded-template
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-go
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-haskell
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-html
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-java
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-javascript
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-jsdoc
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-json
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-julia
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-ocaml
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-php
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-python
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-ql
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-regex
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-ruby
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-rust
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-scala
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-swift
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-toml
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-tsq
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-typescript
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-verilog

cd ..

python build.py
