from glob import glob
from platform import system

from setuptools import Extension, setup  # type: ignore
from wheel.bdist_wheel import bdist_wheel  # type: ignore


class BdistWheel(bdist_wheel):
    def get_tag(self):
        python, abi, platform = super().get_tag()
        if python.startswith("cp"):
            python, abi = "cp39", "abi3"
        return python, abi, platform


sources = glob('tree_sitter_languages/repos/**/src/*.c', recursive=True)
sources.append("tree_sitter_languages/languages.c")

setup(
    packages=["tree_sitter_languages"],
    include_package_data=False,
    ext_modules=[
        Extension(
            name="tree_sitter_languages.languages",
            sources=sources,
            define_macros=[
                ("PY_SSIZE_T_CLEAN", None),
                ("TREE_SITTER_HIDE_SYMBOLS", None),
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
            py_limited_api=True
        )
    ],
    cmdclass={"bdist_wheel": BdistWheel},
)
