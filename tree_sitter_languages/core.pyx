import pathlib
import sys

from tree_sitter import Language, Parser


def get_language(language):
    if sys.platform == 'win32':
        filename = 'languages.dll'
    else:
        filename = 'languages.so'

    binary_path = str(pathlib.Path(__file__).parent / filename)
    language = Language(binary_path, language)
    return language


def get_parser(language):
    language = get_language(language)
    parser = Parser()
    parser.set_language(language)
    return parser
