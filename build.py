from tree_sitter import Language, Parser


Language.build_library(
    'tree_sitter_languages/languages.so',
    [
        'vendor/tree-sitter-go',
        'vendor/tree-sitter-javascript',
        'vendor/tree-sitter-python'
    ]
)
