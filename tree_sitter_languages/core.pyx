import pathlib
import re
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

def get_language_by_filename(name, contents=None):
    matching_keys = []
    for key, entry in compiled_languages.items():
        if 'file-types' not in entry:
            continue
        for ft in entry['file-types']:
            if name == ft or name.endswith(ft):
                matching_keys.append(key)

    if contents is None or not matching_keys:
        return get_language(matching_keys[0]) if matching_keys else None

    best_score = -1
    best_key = None
    for key in matching_keys:
        entry = compiled_languages[key]
        if 'content-regex' in entry and contents is not None:
            match = re.search(entry['content-regex'], contents)
            if match:
                score = match.end() - match.start()
                if score > best_score:
                    best_score = score
                    best_key = key

    return get_language(best_key) if best_key else get_language(matching_keys[0])

def get_parser(language):
    language = get_language(language)
    parser = Parser()
    parser.set_language(language)
    return parser
