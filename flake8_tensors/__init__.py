#!/usr/bin/env python3

__version__ = '0.2.0'
__title__ = 'flake8_tensors'
__summary__ = 'flake8_tensors - flake8 plugin for deep learning codes'
__uri__ = 'https://github.com/dvolgyes/flake8_tensors'
__license__ = 'MIT'
__author__ = 'David Völgyes'
__email__ = 'david.volgyes@ieee.org'

__description__ = """
This program is a flake8 plugin, and recommends some tricks
and best practices for machine learning codes.
"""

from .plugin import Flake8TensorsPlugin

__all__ = ['Flake8TensorsPlugin']
