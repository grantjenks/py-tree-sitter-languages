from collections.abc import Callable
from json import loads
from pathlib import Path
from typing import Any, cast

import pytest
from tree_sitter import Language, Parser

from tree_sitter_language_pack import SupportedLanguage, get_language, get_parser

languages = set(cast(dict[str, Any], loads((Path(__file__).parent.parent.resolve() / "languages.json").read_text())))


@pytest.mark.parametrize("language", languages)
def test_get_language(language: SupportedLanguage) -> None:
    assert isinstance(get_language(language), Language)


@pytest.mark.parametrize("language", languages)
def test_get_parser(language: SupportedLanguage) -> None:
    assert isinstance(get_parser(language), Parser)


@pytest.mark.parametrize("handler", (get_language, get_parser))
def test_raises_exception_for_invalid_name(handler: Callable[[str], Any]) -> None:
    with pytest.raises(LookupError):
        handler("invalid")
