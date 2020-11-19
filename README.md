flake8_tensors
==============

flake8 plugin which recommends some tricks for machine learning codes.

## Installation

The plugin requires python3.8, because the walrus operator was convenient,
and I wrote the plugin for myself. If you don't use python3.8, then it is
time to upgrade. :) Then proceed with:

for stable version:
`pip install flake8_tensors`

for the development:
`pip install git+git://github.com/dvolgyes/flake8_tensors --upgrade`


## Usage

After the code is installed, call flake8 on your project.
The plugin emits warning messages with "WT" prefix, e.g. WT100.

The messages meant to refer best practices, or cool projects,
like [einops](https://github.com/arogozhnikov/einops), [opt_einsum](https://github.com/dgasmith/opt_einsum),
[Adabelief](https://juntang-zhuang.github.io/adabelief/), etc.

If you don't understand a warning, open a ticket, and i will clarify it.
If you have suggestions, let me know. And of course, if you find
a false positive, share the problematic snippet.
(False positives are absolutely possible, actually, quite easy to make one.
But assuming reasonable developer practices, like not calling your variable
as "BatchNorm3d", the false positive rate should be low.)


