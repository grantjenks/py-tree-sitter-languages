"""Tree Sitter with Languages
"""

from tree_sitter import Language, Parser


def get_parser(language):
    language = Language('languages.so', language)
    parser = Parser()
    parser.set_language(language)
    return parser


__version__ = '0.0.0'
