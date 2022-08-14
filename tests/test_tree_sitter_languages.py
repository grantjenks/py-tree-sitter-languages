from tree_sitter_languages import get_language, get_parser

PYTHON_CODE = """
    def foo():
        if bar:
            baz()
""".encode()

PYTHON_QUERY = """
(function_definition
  name: (identifier) @function.def)

(call
  function: (identifier) @function.call)
"""


def test_python():
    language = get_language('python')
    query = language.query(PYTHON_QUERY)
    parser = get_parser('python')
    tree = parser.parse(PYTHON_CODE)
    captures = query.captures(tree.root_node)
    assert len(captures) == 2
    assert captures[0][1] == "function.def"
    assert captures[0][0].text.decode() == 'foo'
    assert captures[1][1] == "function.call"
    assert captures[1][0].text.decode() == 'baz'
