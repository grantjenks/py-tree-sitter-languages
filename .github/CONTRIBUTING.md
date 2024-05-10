# Contributing guidelines

## Adding a new language

- Add the language repo to _README.rst_ (along with its license) and
  _tree_sitter_languages/repos/repos.txt_.
- Add the language name to _tests/test_tree_sitter_languages.py_ (sorted).
- Add `TS_LANGUAGE_INIT(name)` and `TS_LANGUAGE_METHOD(name),` to
  _tree_sitter_languages/languages.c_ (sorted).
- Submit a pull request.
