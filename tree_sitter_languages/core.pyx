import pathlib
import sys

from .generated import compiled_languages
from tree_sitter import Language, Parser


def get_language(language):
    if sys.platform == 'win32':
        filename = 'languages.dll'
    else:
        filename = 'languages.so'

    binary_path = str(pathlib.Path(__file__).parent / filename)
    language = Language(binary_path, language)
    return language

def get_language_by_filename(name):
    for key, entry in compiled_languages.items():
        if 'file-types' not in entry:
            continue
        for ft in entry['file-types']:
            if name == ft or name.endswith(ft):
                return get_language(key)
    return None

def get_parser(language):
    language = get_language(language)
    parser = Parser()
    parser.set_language(language)
    return parser
