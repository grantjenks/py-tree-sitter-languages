from unittest import TestCase

from tree_sitter import Language, Parser
from tree_sitter_languages import get_language, get_parser

LANGUAGES = [
    "dot",
    "elisp",
    "elm",
    "fixed_form_fortran",
    "fortran",
    "gomod",
    "hack",
    "hcl",
    "kotlin",
    "make",
    "objc",
    "rst",
    "scala",
    "sql",
    "terraform",
]


class TestLanguages(TestCase):
    def test_get_parser(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                self.assertIsInstance(get_parser(language), Parser)

    def test_get_language(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                self.assertIsInstance(get_language(language), Language)

    def test_invalid_name(self):
        self.assertRaises(LookupError, get_language, "invalid")
        self.assertRaises(LookupError, get_parser, "invalid")
