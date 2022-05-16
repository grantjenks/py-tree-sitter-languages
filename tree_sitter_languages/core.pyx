import pathlib

from tree_sitter import Language, Parser


def get_language(language):
    binary_path = str(pathlib.Path(__file__).parent / 'languages.so')
    language = Language(binary_path, language)
    return language


def get_parser(language):
    language = get_language(language)
    parser = Parser()
    parser.set_language(language)
    return parser
