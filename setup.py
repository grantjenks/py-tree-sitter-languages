from itertools import chain
from json import loads
from os import chdir, environ, getcwd
from pathlib import Path
from platform import system
from typing import Any, NotRequired, TypedDict

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from wheel.bdist_wheel import bdist_wheel  # type: ignore


class LanguageDict(TypedDict):
    """Language configuration for tree-sitter repositories."""

    repo: str
    branch: NotRequired[str]
    languages: NotRequired[dict[str, str]]


languages: dict[str, LanguageDict] = loads(Path(__file__).with_name("languages.json").read_text())

common_source = Path(__file__).parent / "tree_sitter_language_pack/language.c"


def create_extension(*, languages: set[str]) -> list[Extension]:
    """Create an extension for the given language.

    Args:
        languages (set[str]): The languages to create the extension for.

    Returns:
        Extension: The extension for the language.
    """
    result = []
    for language_name in languages:
        result.append(
            Extension(
                name=f"tree_sitter_language_pack.languages.{language_name}",
                sources=[str(common_source)],
                include_dirs=[language_name],
                define_macros=[
                    ("PY_SSIZE_T_CLEAN", None),
                    ("TREE_SITTER_HIDE_SYMBOLS", None),
                    ("TS_LANGUAGE_NAME", language_name),
                ],
                extra_compile_args=[
                    "-std=c11",
                    "-fvisibility=hidden",
                    "-Wno-cast-function-type",
                    "-Wno-unused-but-set-variable",
                    "-Werror=implicit-function-declaration",
                ]
                if system() != "Windows"
                else [
                    "/std:c11",
                    "/wd4244",
                ],
                py_limited_api=True,
                optional=True,
            )
        )
    return result


extensions: list[Extension] = list(
    chain(
        *(create_extension(languages=set(value.get("languages", {key: ""}).keys())) for key, value in languages.items())
    )
)


class BuildExt(build_ext):
    """Custom build extension to handle tree-sitter language repositories."""

    def build_extension(self, ext: Extension) -> None:
        """Build the extension."""
        ext_name = ext.include_dirs.pop()
        language = languages[ext_name]
        cwd = getcwd()
        directory = Path(cwd) / "vendor" / ext_name
        relative_path = str(directory.relative_to(cwd))
        if directory.is_dir():
            self.spawn(["git", "-C", relative_path, "pull", "-q", "--depth=1"])
        else:
            clone = ["git", "clone", "-q", "--depth=1", "--sparse"]
            if branch := language.get("branch"):
                clone.append(f"--branch={branch}")
            clone.extend([language["repo"], relative_path])
            self.spawn(clone)
            self.spawn(["git", "-C", relative_path, "sparse-checkout", "set", "--no-cone", "/**/src/**"])

        language_name = ext.name.split(".")[-1]
        path = directory / language.get("languages", {language_name: ""})[language_name]
        src = path / "src"

        if "TS_REGENERATE" in environ:
            chdir(path)
            self.spawn(["tree-sitter", "generate", "--no-bindings", "src/grammar.json"])
            chdir(cwd)

        ext.sources.extend(list(map(str, src.glob("*.c"))))
        ext.include_dirs = [str(src)]

        return super().build_extension(ext)


class BdistWheel(bdist_wheel):  # type: ignore[misc]
    """Custom bdist_wheel command to handle Python 3.9 ABI tag."""

    def get_tag(self) -> tuple[Any, Any, Any]:
        """Get the tag for the wheel distribution."""
        python, abi, platform = super().get_tag()
        if python.startswith("cp"):
            python, abi = "cp39", "abi3"
        return python, abi, platform


setup(
    packages=[
        "tree_sitter_language_pack",
        "tree_sitter_language_pack.languages",
    ],
    include_package_data=False,
    ext_modules=extensions,
    cmdclass={
        "build_ext": BuildExt,
        "bdist_wheel": BdistWheel,
    },
)
