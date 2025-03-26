#!/usr/bin/env bash
set -e
cd "$(dirname "$(readlink -f "$0")")/.."

# Sync the parsers and their versions with those used by nvim-treesitter
scripts/update.lua 2>&1 | jq -S . > parsers.json
cp nvim-treesitter/lockfile.json .
git add parsers.json lockfile.json
git config --global user.name 'Github Actions'
git config --global user.email '41898282+github-actions[bot]@users.noreply.github.com'
git commit -m 'Update parsers.json'
git remote set-url origin "https://x-access-token:$GH_TOKEN@github.com/$GITHUB_REPOSITORY"
git push
