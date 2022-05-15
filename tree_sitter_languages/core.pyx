import pathlib

from tree_sitter import Language, Parser


def get_parser(language):
    binary_path = str(pathlib.Path(__file__).parent / 'languages.so')
    language = Language(binary_path, language)
    parser = Parser()
    parser.set_language(language)
    return parser
