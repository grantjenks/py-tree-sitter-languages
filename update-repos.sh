#!/bin/bash
# This script updates repos.txt to use the latest available commits.
# The purpose of repos.txt is to make it easy to see and configure what
# version of each language is used.
set -e

# Create a temporary directory and automatically clean it up when exiting.
tempdir="$(mktemp -d)"
trap 'rm -rf -- "$tempdir"' EXIT

output="$(mktemp)"
cut -d' ' -f1 repos.txt | while read -r url; do
    echo "$url"
    # Find latest commit. https://serverfault.com/a/1054661
    git clone -q --depth=1 "$url" "$tempdir"/repo
    latest_commit=$(cd "$tempdir"/repo && git rev-parse HEAD)
    rm -rf "$tempdir"/repo

    echo "  --> $latest_commit"

    # Save to a temporary file. We can't overwrite repos.txt in the
    # project directory because we could be still reading from it.
    echo "$url $latest_commit" >> "$tempdir"/new_repos.txt
done

mv "$tempdir"/new_repos.txt ./repos.txt
