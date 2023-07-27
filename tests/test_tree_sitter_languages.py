from tree_sitter_languages import get_language, get_parser, get_language_by_filename
from tree_sitter_languages.generated import compiled_languages

LANGUAGES = [
    'bash',
    'c',
    'c_sharp',  # c-sharp
    'commonlisp',
    'cpp',
    'css',
    'dockerfile',
    'dot',
    'elisp',
    'elixir',
    'elm',
    'embedded_template',  # embedded-template
    'erlang',
    'go',
    'gomod',  # go-mod
    'hack',
    'haskell',
    'hcl',
    'html',
    'java',
    'javascript',
    'jsdoc',
    'json',
    'julia',
    'kotlin',
    'lua',
    'make',
    'markdown',
    'objc',
    'ocaml',
    'perl',
    'php',
    'python',
    'ql',
    'r',
    'regex',
    'rst',
    'ruby',
    'rust',
    'scala',
    'sql',
    'sqlite',
    'toml',
    'tsq',
    'tsx',
    'typescript',
    'yaml',
]

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


def test_get_parser():
    for language in LANGUAGES:
        parser = get_parser(language)
        assert parser


def test_get_language():
    for language in LANGUAGES:
        language = get_language(language)
        assert language

def test_generated():
    for language in LANGUAGES:
        assert compiled_languages[language] is not None

def test_get_language_by_filename():
    for filename, lang in {
        'file.sh': 'bash',
    }.items():
        assert get_language_by_filename(filename).name == get_language(lang).name
