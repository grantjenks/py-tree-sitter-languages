from textwrap import dedent
from tree_sitter_languages import get_parser


def test_python():
    parser = get_parser('python')
    python = dedent("""
        def foo():
            if bar:
                baz()
    """).encode()
    tree = parser.parse(python)
    assert tree
