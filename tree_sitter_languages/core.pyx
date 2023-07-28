import pathlib
import re
import sys

from .generated import index
from tree_sitter import Language, Parser


def get_language(language):
    if sys.platform == 'win32':
        filename = 'languages.dll'
    else:
        filename = 'languages.so'

    binary_path = str(pathlib.Path(__file__).parent / filename)
    language = Language(binary_path, language)
    return language

def get_language_for_file(file_name, file_contents=None):
    name = Language.lookup_language_name_by_file(index, file_name, file_contents)
    return get_language(name) if name is not None else None

def get_parser(language):
    language = get_language(language)
    parser = Parser()
    parser.set_language(language)
    return parser
