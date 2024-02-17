import json
import os
import subprocess
import sys
from tree_sitter import Language

with open("parsers.json") as f:
    parsers = json.load(f)
with open("lockfile.json") as f:
    lockfile = json.load(f)

repos = []
vendors = []
# https://github.com/tree-sitter/py-tree-sitter/issues/189
disabled_langs = [
    "vue",  # html, angular
    "angular",  # html
    "purescript",  # haskell, unison
    "unison",  # haskell
    "terraform",  # hcl
    "svelte",  # org
    "beancount",  # org
]
for lang, data in parsers.items():
    if lang in disabled_langs:
        continue
    url = data["install_info"]["url"]
    commit = lockfile[lang]["revision"]
    clone_directory = os.path.join("vendor", url.rstrip("/").split("/")[-1])
    requires_generate_from_grammar = data["install_info"].get("requires_generate_from_grammar", False)
    location = data["install_info"].get("location")
    vendor = clone_directory + "/" + location if location else clone_directory
    repos.append((url, commit, clone_directory, vendor if requires_generate_from_grammar else None))
    vendors.append(vendor)

# During the build, this script runs several times, and only needs to download
# repositories on first time.
if os.path.isdir("vendor") and len(os.listdir("vendor")) == len(repos):
    print(f"{sys.argv[0]}: Language repositories have been cloned already.")
else:
    os.makedirs("vendor", exist_ok=True)
    for url, commit, clone_directory, vendor in repos:
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
        if vendor:
            subprocess.check_call(["tree-sitter", "generate"], cwd=vendor)

print()

if sys.platform == "win32":
    languages_filename = "tree_sitter_languages\\languages.dll"
else:
    languages_filename = "tree_sitter_languages/languages.so"

print(f"{sys.argv[0]}: Building", languages_filename)
Language.build_library(
    languages_filename,
    vendors
)
