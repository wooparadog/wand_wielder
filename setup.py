#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import dirname, realpath, join

CURRENT_DIR = dirname(realpath(__file__))

with open(join(CURRENT_DIR, "wand_wielder/__init__.py")) as package_file:
    version = next(eval(line.split("=")[-1])
                   for line in package_file if line.startswith("__version__"))

setup(
    name="wand_wielder",
    packages=find_packages(),
    version=version,
    description="Image processing in a `dict` config way, using wand",
    author="Haochuan Guo",
    author_email="guohaochuan@douban.com",
    url="https://github.com/douban/brownant",
    license="MIT",
    keywords=["image processing", "web data"],
    install_requires=[
        "wand >= 0.3.7",
        ],
)
