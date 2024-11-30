flake8_tensors
==============

[![pyversion](https://img.shields.io/pypi/pyversions/flake8_tensors.svg)](https://pypi.org/project/flake8_tensors/)
[![PyPI - License](https://img.shields.io/pypi/l/flake8_tensors.svg)](https://github.com/dvolgyes/flake8_tensors/raw/master/LICENSE.txt)

flake8 plugin which recommends some tricks for machine learning codes.

## Installation

The plugin requires python3.8+.

Install the stable version:
`pip install flake8_tensors --upgrade`

Or with pipx:
`pipx install flake8`
`pipx inject flake8 flake8_tensors`

## Usage

After the code is installed, call flake8 on your project.
The plugin emits warning messages with "WT" prefix, e.g. WT100.

The messages meant to refer my opinionated best practices, or cool projects,
like [einops](https://github.com/arogozhnikov/einops), [opt_einsum](https://github.com/dgasmith/opt_einsum),
[Adabelief](https://juntang-zhuang.github.io/adabelief/), etc.

If you don't understand a warning, open a ticket, and i will clarify it.
If you have suggestions, let me know. And of course, if you find
a false positive, share the problematic snippet.
(False positives are absolutely possible, actually, quite easy to make one.
But assuming reasonable developer practices, like not calling your variable
as "BatchNorm3d", the false positive rate should be low.)
