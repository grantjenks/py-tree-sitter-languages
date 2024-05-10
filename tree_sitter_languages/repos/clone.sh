#!/bin/bash -e

while read -r repo; do
    name="${repo##*/tree-sitter-}"
    [[ ! -d "$name" ]] || rm -fr "$name"
    args=(--depth=1 --sparse)
    if [[ $name == fixed-form-fortran ]]; then
        args+=(--branch=f77)
    elif [[ $name == sql ]]; then
        args+=(--branch=gh-pages)
    fi
    git clone "${args[@]}" "$repo" "$name"
    git -C "$name" sparse-checkout set --no-cone '/**/src/**'
    while read -r file; do
        printf 'Patching #include in file: %s\n' "$file" >&2
        if [[ ${file%/*} != rst/src/tree_sitter_rst ]]; then
            sed -i'' -e 's|<tree_sitter/parser.h>|"./tree_sitter/parser.h"|' "$file"
        else
            sed -i'' -e 's|<tree_sitter/parser.h>|"../tree_sitter/parser.h"|' "$file"
        fi
        if [[ $file =~ hcl/.+/scanner[.]c ]]; then
            printf 'Patching symbols in file: %s\n' "$file" >&2
            sed -i'' -e 's/^String string_new/static inline &/' "$file"
        fi
    done < <(grep -rl '<tree_sitter/parser.h>' --exclude "${0##*/}")
done < repos.txt
