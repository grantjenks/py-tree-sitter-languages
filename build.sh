pip install -e .

mkdir vendor
cd vendor
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-go
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-javascript
git clone --depth 1 https://github.com/tree-sitter/tree-sitter-python
cd ..

python build.py
