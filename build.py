import json
import os
import glob
import pprint
import re
import subprocess
import sys
from tree_sitter import Language


repos = []
with open("repos.txt", "r") as file:
    for line in file:
        url, commit = line.split()
        clone_directory = os.path.join("vendor", url.rstrip("/").split("/")[-1])
        repos.append((url, commit, clone_directory))

# During the build, this script runs several times, and only needs to download
# repositories on first time.
if os.path.isdir("vendor") and len(os.listdir("vendor")) == len(repos):
    print(f"{sys.argv[0]}: Language repositories have been cloned already.")
else:
    os.makedirs("vendor", exist_ok=True)
    for url, commit, clone_directory in repos:
        print()
        print(f"{sys.argv[0]}: Cloning: {url} (commit {commit}) --> {clone_directory}")
        print()

        if os.path.exists(clone_directory):
            continue

        # https://serverfault.com/a/713065
        os.mkdir(clone_directory)
        subprocess.check_call(["git", "init"], cwd=clone_directory)
        subprocess.check_call(["git", "remote", "add", "origin", url], cwd=clone_directory)
        subprocess.check_call(["git", "fetch", "--depth=1", "origin", commit], cwd=clone_directory)
        subprocess.check_call(["git", "checkout", commit], cwd=clone_directory)


langs = {}
for _, _, clone_directory in repos:
    keys = []
    for parser_path in glob.glob(os.path.join(clone_directory, "**/parser.c"), recursive=True):
        with open(parser_path, 'r') as parser:
            for line in parser:
                if line.startswith("extern const TSLanguage *tree_sitter_"):
                    key = re.search(r"tree_sitter_(.+?)\(", line).group(1)
                    keys.append(key)
    package_json_path = os.path.join(clone_directory, 'package.json')
    if not os.path.isfile(package_json_path):
        for key in keys:
            langs[key] = {}
        continue
    with open(package_json_path, 'r') as file:
        package_json = json.load(file)
        if 'tree-sitter' not in package_json:
            for key in keys:
                langs[key] = {}
            continue
        for entry in package_json['tree-sitter']:
            if len(keys) == 1:
                langs[keys[0]] = entry
                continue
            for key in keys:
                if entry['scope'].endswith(key) or ('path' in entry and entry['path'] == key):
                    langs[key] = entry
                    break

with open('tree_sitter_languages/generated.pyx', 'w') as file:
    file.write('compiled_languages = ')
    pprint.pprint(langs, stream=file)


if sys.platform == "win32":
    languages_filename = "tree_sitter_languages\\languages.dll"
else:
    languages_filename = "tree_sitter_languages/languages.so"

print(f"{sys.argv[0]}: Building", languages_filename)
Language.build_library(
    languages_filename,
    [
        'vendor/tree-sitter-bash',
        'vendor/tree-sitter-c',
        'vendor/tree-sitter-c-sharp',
        'vendor/tree-sitter-commonlisp',
        'vendor/tree-sitter-cpp',
        'vendor/tree-sitter-css',
        'vendor/tree-sitter-dockerfile',
        'vendor/tree-sitter-dot',
        'vendor/tree-sitter-elisp',
        'vendor/tree-sitter-elixir',
        'vendor/tree-sitter-elm',
        'vendor/tree-sitter-embedded-template',
        'vendor/tree-sitter-erlang',
        'vendor/tree-sitter-go',
        'vendor/tree-sitter-go-mod',
        'vendor/tree-sitter-hack',
        'vendor/tree-sitter-haskell',
        'vendor/tree-sitter-hcl',
        'vendor/tree-sitter-html',
        'vendor/tree-sitter-java',
        'vendor/tree-sitter-javascript',
        'vendor/tree-sitter-jsdoc',
        'vendor/tree-sitter-json',
        'vendor/tree-sitter-julia',
        'vendor/tree-sitter-kotlin',
        'vendor/tree-sitter-lua',
        'vendor/tree-sitter-make',
        'vendor/tree-sitter-markdown',
        'vendor/tree-sitter-objc',
        'vendor/tree-sitter-ocaml/ocaml',
        'vendor/tree-sitter-perl',
        'vendor/tree-sitter-php',
        'vendor/tree-sitter-python',
        'vendor/tree-sitter-ql',
        'vendor/tree-sitter-r',
        'vendor/tree-sitter-regex',
        'vendor/tree-sitter-rst',
        'vendor/tree-sitter-ruby',
        'vendor/tree-sitter-rust',
        'vendor/tree-sitter-scala',
        'vendor/tree-sitter-sql',
        'vendor/tree-sitter-sqlite',
        'vendor/tree-sitter-toml',
        'vendor/tree-sitter-tsq',
        'vendor/tree-sitter-typescript/tsx',
        'vendor/tree-sitter-typescript/typescript',
        'vendor/tree-sitter-yaml',
    ]
)
