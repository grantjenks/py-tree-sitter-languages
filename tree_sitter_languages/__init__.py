"""Tree-sitter languages"""

from tree_sitter import Language, Parser

from . import languages


def get_language(name: str) -> Language:
    """Get the language with the given name."""
    if not hasattr(languages, name):
        raise AttributeError(f"Language not found: {name}")
    return Language(getattr(languages, name)())


def get_parser(language: str) -> Parser:
    """Get a parser for the given language name."""
    return Parser(get_language(language))


__all__ = ["get_language", "get_parser"]
