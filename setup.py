from json import loads
from pathlib import Path
from platform import system
from os import chdir, environ, getcwd
from typing import TypedDict

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from wheel.bdist_wheel import bdist_wheel

Language = TypedDict("Language", {
    "repo": str,
    "branch": str | None,
    "languages": dict[str, str] | None
})

languages: dict[str, Language] = \
    loads(Path(__file__).with_name("languages.json").read_text())

extensions: list[Extension] = []

common_source = Path(__file__).parent / "tree_sitter_languages" / "language.c"

for lang, data in languages.items():
    for name in data.get("languages", {lang: ""}).keys():
        extensions.append(
            Extension(
                name=f"tree_sitter_languages._language.{name}",
                sources=[str(common_source)],
                include_dirs=[lang],
                define_macros=[
                    ("PY_SSIZE_T_CLEAN", None),
                    ("TREE_SITTER_HIDE_SYMBOLS", None),
                    ("TS_LANGUAGE_NAME", name),
                ],
                extra_compile_args=[
                    "-std=c11",
                    "-fvisibility=hidden",
                    "-Wno-cast-function-type",
                    "-Wno-unused-but-set-variable",
                    "-Werror=implicit-function-declaration",
                ] if system() != "Windows" else [
                    "/std:c11",
                    "/wd4244",
                ],
                py_limited_api=True,
                optional=True,
            )
        )


class BuildExt(build_ext):
    def build_extension(self, ext: Extension):
        name = ext.include_dirs.pop()
        lang = languages[name]
        cwd = getcwd()

        if not (dir := Path(cwd) / "vendor" / name).is_dir():
            clone = ["git", "clone", "-q", "--depth=1", "--sparse"]
            if branch := lang.get("branch"):
                clone.append(f"--branch={branch}")
            clone.extend([lang["repo"], dir.relative_to(cwd)])
            self.spawn(clone)
            self.spawn([
                "git", "-C", dir.relative_to(cwd),
                "sparse-checkout", "set", "--no-cone", "/**/src/**"
            ])
        else:
            self.spawn([
                "git", "-C", dir.relative_to(cwd),
                "pull", "-q", "--depth=1"
            ])

        name = ext.name.split(".")[-1]
        path = dir / lang.get("languages", {name: ""})[name]
        src = path / "src"
        if "TS_REGENERATE" in environ:
            chdir(path)
            self.spawn([
                "tree-sitter", "generate",
                "--no-bindings", "src/grammar.json"
            ])
            chdir(cwd)
        ext.sources.extend(list(map(str, src.glob("*.c"))))
        ext.include_dirs = [str(src)]

        return super().build_extension(ext)


class BdistWheel(bdist_wheel):
    def get_tag(self):
        python, abi, platform = super().get_tag()
        if python.startswith("cp"):
            python, abi = "cp39", "abi3"
        return python, abi, platform


setup(
    packages=[
        "tree_sitter_languages",
        "tree_sitter_languages._language",
    ],
    include_package_data=False,
    ext_modules=extensions,
    cmdclass={
        "build_ext": BuildExt,
        "bdist_wheel": BdistWheel,
    },
)
