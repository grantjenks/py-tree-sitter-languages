=====================
Tree-sitter languages
=====================

Binary Python wheels for many tree-sitter languages.

`py-tree-sitter`_ is a fantastic library that provides Python bindings for the
even more fantastic `tree-sitter`_ parsing library.

`py-tree-sitter-languages`_ provides binary Python wheels for many tree sitter
languages that do not have their own packages.

Install
=======

.. code:: bash

   pip install tree-sitter-languages

Usage
=====

.. code:: python

   from tree_sitter_languages import get_language, get_parser

   language = get_language("rst")
   parser = get_parser("rst")

That's the whole API!

Refer to `py-tree-sitter`_ for the language and parser API.

License
=======

This project is licensed under the `Apache License, Version 2.0`_.

.. _`Apache License, Version 2.0`: http://www.apache.org/licenses/LICENSE-2.0

It also includes the following other projects distributed in binary form:

* https://github.com/tree-sitter/tree-sitter — licensed under the MIT License.
* https://github.com/rydesun/tree-sitter-dot — licensed under the MIT License.
* https://github.com/Wilfred/tree-sitter-elisp — licensed under the MIT License.
* https://github.com/elm-tooling/tree-sitter-elm — licensed under the MIT
  License.
* https://github.com/ZedThree/tree-sitter-fixed-form-fortran - licensed under
  the MIT License.
* https://github.com/stadelmanma/tree-sitter-fortran - licensed under the MIT
  License.
* https://github.com/camdencheek/tree-sitter-go-mod — licensed under the MIT
  License.
* https://github.com/slackhq/tree-sitter-hack — licensed under the MIT License.
* https://github.com/tree-sitter-grammars/tree-sitter-hcl - licensed under the
  Apache License, Version 2.0.
* https://github.com/fwcd/tree-sitter-kotlin — licensed under the MIT License.
* https://github.com/tree-sitter-grammars/tree-sitter-make — licensed under the
  MIT License.
* https://github.com/tree-sitter-grammars/tree-sitter-objc - licensed under the
  MIT License.
* https://github.com/tree-sitter-grammars/tree-sitter-objc — licensed under the
  MIT License.
* https://github.com/stsewd/tree-sitter-rst - licensed under the MIT License.
* https://github.com/tree-sitter/tree-sitter-scala — licensed under the MIT
  License.
* https://github.com/derekstride/tree-sitter-sql — licensed under the MIT
  License.

.. _`tree-sitter`: https://tree-sitter.github.io/
.. _`py-tree-sitter`: https://github.com/tree-sitter/py-tree-sitter
.. _`py-tree-sitter-languages`:
   https://github.com/grantjenks/py-tree-sitter-languages
