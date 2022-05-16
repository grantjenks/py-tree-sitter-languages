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

2. build.sh — Shell script to download support for all languages.

3. build.py — Python script to build support for all languages.

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

.. _`tree-sitter`: https://tree-sitter.github.io/
