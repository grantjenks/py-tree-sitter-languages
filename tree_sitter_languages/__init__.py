"""Tree-sitter languages"""

from importlib import import_module as _import

from tree_sitter import Language, Parser


def get_language(name: str) -> Language:
    """Get the language with the given name."""
    try:
        module = _import(f"._language.{name}", __package__)
    except ModuleNotFoundError:
        raise LookupError(f"Language not found: {name}")
    else:
        return Language(module.language())


def get_parser(language: str) -> Parser:
    """Get a parser for the given language name."""
    return Parser(get_language(language))


__all__ = ["get_language", "get_parser"]
