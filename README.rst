==================================================
Python Bindings for Tree Sitter with All Languages
==================================================

Binary Python wheels for all tree sitter languages.

`py-tree-sitter`_ is a fantastic library that provides Python bindings for the
even more fantastic `tree-sitter`_ parsing library.

`py-tree-sitter-languages`_ provides binary Python wheels for all tree sitter
languages. The binary wheels remove the need to download and compile support
for individual languages.

.. _`py-tree-sitter-languages`: https://github.com/grantjenks/py-tree-sitter-languages


Install
=======

::

   pip install tree_sitter_languages

Source installs are not supported. To see how the binary wheels are built, look
at:

1. setup.py — Python package setup.

2. repos.txt — Text file that contains a list of included language repositories and their commit hashes.

3. build.py — Python script to download and build the language repositories.

4. .github/workflows/release.yml — GitHub action to invoke `cibuildwheel`_ and
   release to PyPI.

.. _`cibuildwheel`: https://github.com/pypa/cibuildwheel


Usage
=====

::

   from tree_sitter_languages import get_language, get_parser

   language = get_language('python')
   parser = get_parser('python')

That's the whole API!

Refer to `py-tree-sitter`_ for the language and parser API. Notice the
``Language.build_library(...)`` step can be skipped! The binary wheel includes
the language binary.

.. _`py-tree-sitter`: https://github.com/tree-sitter/py-tree-sitter


Demo
====

Want to know something crazy? Python lacks multi-line comments. Whhaaa!?!

It's really not such a big deal. Instead of writing::

   """
   My awesome
   multi-line
   comment.
   """

Simply write::

   # My awesome
   # multi-line
   # comment.

So multi-line comments are made by putting multiple single-line comments in
sequence. Amazing!

Now, how to find all the strings being used as comments?

Start with some example Python code::

   example = """
   #!shebang
   # License blah blah (Apache 2.0)
   "This is a module docstring."

   a = 1

   '''This
   is
   not
   a
   multiline
   comment.'''

   b = 2

   class Test:
       "This is a class docstring."

       'This is bogus.'

       def test(self):
           "This is a function docstring."

           "Please, no."

           return 1

   c = 3
   """

Notice a couple things:

1. Python has module, class, and function docstrings that bare a striking
   resemblance to the phony string comments.

2. Python supports single-quoted, double-quoted, triple-single-quoted, and
   triple-double-quoted strings (not to mention prefixes for raw strings,
   unicode strings, and more).

Creating a regular expression to capture the phony string comments would be
exceedingly difficult!

Enter `tree-sitter`_::

   from tree_sitter_languages import get_language, get_parser

   language = get_language('python')
   parser = get_parser('python')

Tree-sitter creates an abstract syntax tree (actually, a `concrete syntax
tree`_) and supports queries::

   tree = parser.parse(example.encode())
   node = tree.root_node
   print(node.sexp())

.. _`concrete syntax tree`: https://stackoverflow.com/q/1888854/232571

Look for statements that are a single string expression::

   stmt_str_pattern = '(expression_statement (string)) @stmt_str'
   stmt_str_query = language.query(stmt_str_pattern)
   stmt_strs = stmt_str_query.captures(node)
   stmt_str_points = set(
       (node.start_point, node.end_point) for node, _ in stmt_strs
   )
   print(stmt_str_points)

Now, find those statement string expressions that are actually module, class,
or function docstrings::

   doc_str_pattern = """
       (module . (comment)* . (expression_statement (string)) @module_doc_str)

       (class_definition
           body: (block . (expression_statement (string)) @class_doc_str))

       (function_definition
           body: (block . (expression_statement (string)) @function_doc_str))
   """
   doc_str_query = language.query(doc_str_pattern)
   doc_strs = doc_str_query.captures(node)
   doc_str_points = set(
       (node.start_point, node.end_point) for node, _ in doc_strs
   )

With the set of string expression statements and the set of docstring
statements, the locations of all phony string comments is::

   comment_strs = stmt_str_points - doc_str_points
   print(sorted(comment_strs))


License
=======

Copyright 2022-2023 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

The project also includes `the corresponding projects <repos.txt>`_ distributed in binary
form:

.. _`tree-sitter`: https://tree-sitter.github.io/

* https://git.sr.ht/~rockorager/tree-sitter-scfg — licensed under the MIT License
* https://git.sr.ht/~yotam/tree-sitter-smali — licensed under the MIT License
* https://gitlab.com/WhyNotHugo/tree-sitter-jsonc.git — licensed under the MIT License
* https://gitlab.com/gabmus/tree-sitter-blueprint.git — licensed under the GNU General Public License v3.0
* https://gitlab.com/jirgn/tree-sitter-fusion.git — licensed under the MIT License
* https://gitlab.com/xasc/tree-sitter-t32.git — licensed under the MIT License
* https://github.com/6cdh/tree-sitter-racket — licensed under the MIT License
* https://github.com/6cdh/tree-sitter-scheme — licensed under the MIT License
* https://github.com/AlexanderBrevig/tree-sitter-forth — licensed under the MIT License
* https://github.com/Beaglefoot/tree-sitter-awk — licensed under the MIT License
* https://github.com/BonaBeavis/tree-sitter-sparql — licensed under the MIT License
* https://github.com/BonaBeavis/tree-sitter-turtle — licensed under the MIT License
* https://github.com/ColinKennedy/tree-sitter-objdump — licensed under the GNU General Public License v3.0
* https://github.com/ColinKennedy/tree-sitter-usd — licensed under the GNU General Public License v3.0
* https://github.com/CyberShadow/tree-sitter-d — licensed under the BSL License v1.0
* https://github.com/Decodetalkers/tree-sitter-groovy — licensed under the MIT License
* https://github.com/Decodetalkers/tree-sitter-meson — licensed under the MIT License
* https://github.com/Decodetalkers/tree-sitter-qmldir — licensed under the MIT License
* https://github.com/FallenAngel97/tree-sitter-rego — licensed under the MIT License
* https://github.com/FoamScience/tree-sitter-foam — licensed under the MIT License
* https://github.com/Fymyte/tree-sitter-rasi — licensed under the MIT License
* https://github.com/Himujjal/tree-sitter-svelte — licensed under the MIT License
* https://github.com/Hubro/tree-sitter-robot — licensed under the ISC License
* https://github.com/Hubro/tree-sitter-yang — licensed under the Apache License 2.0
* https://github.com/Isopod/tree-sitter-pascal.git — licensed under the MIT License
* https://github.com/Joakker/tree-sitter-json5 — licensed under the MIT License
* https://github.com/JoranHonig/tree-sitter-solidity — licensed under the MIT License
* https://github.com/Kerl13/tree-sitter-menhir — licensed under the MIT License
* https://github.com/MDeiml/tree-sitter-markdown — licensed under the MIT License
* https://github.com/MercuryTechnologies/tree-sitter-haskell-persistent — licensed under the MIT License
* https://github.com/MichaHoffmann/tree-sitter-hcl — licensed under the Apache License 2.0
* https://github.com/MichaHoffmann/tree-sitter-promql — licensed under the Apache License 2.0
* https://github.com/MunifTanjim/tree-sitter-lua — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-arduino — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-chatito — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-gitattributes — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-gpg-config — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-pem — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-poe-filter — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-pymanifest — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-requirements — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-ssh-config — licensed under the MIT License
* https://github.com/ObserverOfTime/tree-sitter-xml — licensed under the MIT License
* https://github.com/PRQL/tree-sitter-prql — licensed under the MIT License
* https://github.com/Philipp-M/tree-sitter-ungrammar — licensed under the MIT License
* https://github.com/Philipp-M/tree-sitter-yuck — licensed under the MIT License
* https://github.com/PorterAtGoogle/tree-sitter-textproto — licensed under the ISC License
* https://github.com/PrestonKnopp/tree-sitter-gdscript — licensed under the MIT License
* https://github.com/PrestonKnopp/tree-sitter-godot-resource — licensed under the MIT License
* https://github.com/RaafatTurki/tree-sitter-sxhkdrc — licensed under the MIT License
* https://github.com/RubixDev/ebnf — licensed under the GNU General Public License v3.0
* https://github.com/Teddytrombone/tree-sitter-typoscript — licensed under the MIT License
* https://github.com/UserNobody14/tree-sitter-dart — licensed under the MIT License
* https://github.com/WhatsApp/tree-sitter-erlang — licensed under the Apache License 2.0
* https://github.com/acristoffers/tree-sitter-matlab — licensed under the MIT License
* https://github.com/addcninblue/tree-sitter-cooklang — licensed under the ISC License
* https://github.com/aheber/tree-sitter-sfapex — licensed under the MIT License
* https://github.com/alemuller/tree-sitter-make — licensed under the MIT License
* https://github.com/alemuller/tree-sitter-ninja — licensed under the MIT License
* https://github.com/alex-pinkus/tree-sitter-swift — licensed under the MIT License
* https://github.com/alexlafroscia/tree-sitter-glimmer — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-bass — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-bicep — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-bitbake — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-cairo — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-capnp — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-cpon — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-csv — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-doxygen — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-firrtl — licensed under the Apache License 2.0
* https://github.com/amaanq/tree-sitter-func — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-gn — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-go-sum — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-hare — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-kconfig — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-kdl — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-luadoc — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-luap — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-luau — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-nqc — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-objc — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-odin — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-pony — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-puppet — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-re2c — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-ron — licensed under the Apache License 2.0
* https://github.com/amaanq/tree-sitter-squirrel — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-starlark — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-tablegen — licensed under the MIT License
* https://github.com/amaanq/tree-sitter-uxntal — licensed under the MIT License
* https://github.com/ambroisie/tree-sitter-tiger — licensed under the MIT License
* https://github.com/antosha417/tree-sitter-hocon — licensed under the MIT License
* https://github.com/arnarg/tree-sitter-todotxt.git — licensed under the MIT License
* https://github.com/artagnon/tree-sitter-mlir — licensed under the Apache License 2.0
* https://github.com/ath3/tree-sitter-passwd — licensed under the The Unlicense
* https://github.com/atom-ocaml/tree-sitter-ocamllex — licensed under the MIT License
* https://github.com/bamonroe/tree-sitter-rnoweb — licensed under the MIT License
* https://github.com/benwilliamgraham/tree-sitter-llvm — licensed under the MIT License
* https://github.com/bkegley/tree-sitter-graphql — licensed under the MIT License
* https://github.com/briot/tree-sitter-ada — licensed under the MIT License
* https://github.com/camdencheek/tree-sitter-dockerfile — licensed under the MIT License
* https://github.com/camdencheek/tree-sitter-go-mod — licensed under the MIT License
* https://github.com/cbarrete/tree-sitter-ledger — licensed under the MIT License
* https://github.com/charmbracelet/tree-sitter-vhs — licensed under the MIT License
* https://github.com/claytonrcarter/tree-sitter-phpdoc — licensed under the MIT License
* https://github.com/connorlay/tree-sitter-eex — licensed under the MIT License
* https://github.com/connorlay/tree-sitter-heex — licensed under the MIT License
* https://github.com/connorlay/tree-sitter-surface — licensed under the MIT License
* https://github.com/cstrahan/tree-sitter-nix — licensed under the MIT License
* https://github.com/derekstride/tree-sitter-sql — licensed under the MIT License
* https://github.com/duskmoon314/tree-sitter-thrift — licensed under the MIT License
* https://github.com/elixir-lang/tree-sitter-elixir — licensed under the Apache License 2.0
* https://github.com/elm-tooling/tree-sitter-elm — licensed under the MIT License
* https://github.com/elves/tree-sitter-elvish — licensed under the BSD Zero Clause License
* https://github.com/eonpatapon/tree-sitter-cue — licensed under the MIT License
* https://github.com/erasin/tree-sitter-po — licensed under the MIT License
* https://github.com/euclidianAce/tree-sitter-teal — licensed under the MIT License
* https://github.com/fab4100/tree-sitter-ispc — licensed under the MIT License
* https://github.com/flurie/tree-sitter-jq — licensed under the BSD 3-Clause "New" or "Revised" License
* https://github.com/fwcd/tree-sitter-kotlin — licensed under the MIT License
* https://github.com/gbprod/tree-sitter-gitcommit — licensed under the Do What The F*ck You Want To Public License
* https://github.com/gbprod/tree-sitter-twig — licensed under the Do What The F*ck You Want To Public License
* https://github.com/glapa-grossklag/tree-sitter-elsa — licensed under the MIT License
* https://github.com/gleam-lang/tree-sitter-gleam — licensed under the Apache License 2.0
* https://github.com/grahambates/tree-sitter-m68k — licensed under the MIT License
* https://github.com/ikatyang/tree-sitter-toml — licensed under the MIT License
* https://github.com/ikatyang/tree-sitter-vue — licensed under the MIT License
* https://github.com/ikatyang/tree-sitter-yaml — licensed under the MIT License
* https://github.com/indoorvivants/tree-sitter-smithy — licensed under the MIT License
* https://github.com/interdependence/tree-sitter-htmldjango — licensed under the MIT License
* https://github.com/jakestanger/tree-sitter-corn — licensed under the MIT License
* https://github.com/jbellerb/tree-sitter-dhall — licensed under the MIT License
* https://github.com/joelspadin/tree-sitter-devicetree — licensed under the MIT License
* https://github.com/jrmoulton/tree-sitter-slint — licensed under the MIT License
* https://github.com/justinmk/tree-sitter-ini — licensed under the Apache License 2.0
* https://github.com/kylegoetz/tree-sitter-unison — licensed under the MIT License
* https://github.com/latex-lsp/tree-sitter-bibtex — licensed under the MIT License
* https://github.com/latex-lsp/tree-sitter-latex — licensed under the MIT License
* https://github.com/leo60228/tree-sitter-pioasm — licensed under the MIT License
* https://github.com/madskjeldgaard/tree-sitter-supercollider — licensed under the MIT License
* https://github.com/maxxnino/tree-sitter-zig — licensed under the MIT License
* https://github.com/mgramigna/tree-sitter-fsh — licensed under the MIT License
* https://github.com/milisims/tree-sitter-org — licensed under the MIT License
* https://github.com/mleonidas/tree-sitter-authzed — licensed under the MIT License
* https://github.com/monaqa/tree-sitter-mermaid — licensed under the MIT License
* https://github.com/naclsn/tree-sitter-nasm — licensed under the MIT License
* https://github.com/neovim/tree-sitter-vim — licensed under the MIT License
* https://github.com/neovim/tree-sitter-vimdoc — licensed under the Apache License 2.0
* https://github.com/nickel-lang/tree-sitter-nickel — licensed under the MIT License
* https://github.com/nvim-neorg/tree-sitter-norg — licensed under the MIT License
* https://github.com/nvim-treesitter/tree-sitter-query — licensed under the Apache License 2.0
* https://github.com/ok-ryoko/tree-sitter-systemtap — licensed under the MIT License
* https://github.com/omertuc/tree-sitter-go-work — licensed under the MIT License
* https://github.com/osthomas/tree-sitter-snakemake — licensed under the MIT License
* https://github.com/pfeiferj/tree-sitter-hurl — licensed under the Apache License 2.0
* https://github.com/polarmutex/tree-sitter-beancount — licensed under the MIT License
* https://github.com/r-lib/tree-sitter-r — licensed under the MIT License
* https://github.com/r001/tree-sitter-leo — licensed under the Apache License 2.0
* https://github.com/ram02z/tree-sitter-fish — licensed under the The Unlicense
* https://github.com/rest-nvim/tree-sitter-http — licensed under the MIT License
* https://github.com/rydesun/tree-sitter-dot — licensed under the MIT License
* https://github.com/savonet/tree-sitter-liquidsoap — licensed under the MIT License
* https://github.com/serenadeai/tree-sitter-scss — licensed under the MIT License
* https://github.com/shunsambongi/tree-sitter-gitignore — licensed under the MIT License
* https://github.com/sigmaSd/tree-sitter-strace — licensed under the MIT License
* https://github.com/slackhq/tree-sitter-hack — licensed under the MIT License
* https://github.com/sogaiu/tree-sitter-clojure — licensed under the Creative Commons Zero v1.0 Universal
* https://github.com/sogaiu/tree-sitter-janet-simple — licensed under the Other License
* https://github.com/sourcegraph/tree-sitter-jsonnet — licensed under the MIT License
* https://github.com/stadelmanma/tree-sitter-fortran — licensed under the MIT License
* https://github.com/stsewd/tree-sitter-comment — licensed under the MIT License
* https://github.com/stsewd/tree-sitter-rst — licensed under the MIT License
* https://github.com/szebniok/tree-sitter-wgsl — licensed under the MIT License
* https://github.com/the-mikedavis/tree-sitter-diff — licensed under the MIT License
* https://github.com/the-mikedavis/tree-sitter-git-config — licensed under the MIT License
* https://github.com/the-mikedavis/tree-sitter-git-rebase — licensed under the MIT License
* https://github.com/theHamsta/tree-sitter-commonlisp — licensed under the MIT License
* https://github.com/theHamsta/tree-sitter-cuda — licensed under the MIT License
* https://github.com/theHamsta/tree-sitter-glsl — licensed under the MIT License
* https://github.com/theHamsta/tree-sitter-gstlaunch — licensed under the MIT License
* https://github.com/theHamsta/tree-sitter-hlsl — licensed under the MIT License
* https://github.com/theHamsta/tree-sitter-wgsl-bevy — licensed under the MIT License
* https://github.com/tlaplus-community/tree-sitter-tlaplus — licensed under the MIT License
* https://github.com/travonted/tree-sitter-fennel — licensed under the MIT License
* https://github.com/traxys/tree-sitter-lalrpop — licensed under the MIT License
* https://github.com/tree-sitter-perl/tree-sitter-perl — licensed under the Artistic License 2.0
* https://github.com/tree-sitter-perl/tree-sitter-pod — licensed under the Artistic License 2.0
* https://github.com/tree-sitter/tree-sitter-agda — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-bash — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-c — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-c-sharp — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-cpp — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-css — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-embedded-template — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-go — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-haskell — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-html — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-java — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-javascript — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-jsdoc — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-json — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-julia — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-ocaml — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-php — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-python — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-ql — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-regex — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-ruby — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-rust — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-scala — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-typescript — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-verilog — licensed under the MIT License
* https://github.com/treywood/tree-sitter-proto — licensed under the MIT License
* https://github.com/urbit-pilled/tree-sitter-hoon — licensed under the BSD 3-Clause "New" or "Revised" License
* https://github.com/uyha/tree-sitter-cmake — licensed under the MIT License
* https://github.com/uyha/tree-sitter-eds — licensed under the MIT License
* https://github.com/v-analyzer/v-analyzer — licensed under the MIT License
* https://github.com/vala-lang/tree-sitter-vala — licensed under the GNU Lesser General Public License v2.1
* https://github.com/victorhqc/tree-sitter-prisma — licensed under the MIT License
* https://github.com/virchau13/tree-sitter-astro — licensed under the MIT License
* https://github.com/winglang/wing — licensed under the Other License
* https://github.com/winston0410/tree-sitter-hjson — licensed under the MIT License
* https://github.com/yuja/tree-sitter-qmljs — licensed under the MIT License
* https://github.com/zealot128/tree-sitter-pug — licensed under the MIT License
* https://github.com/tree-sitter/tree-sitter-tsq — licensed under the MIT License
