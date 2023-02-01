#!/usr/bin/env python3
import pkg_resources
__version__ = pkg_resources.require('flake8_tensors')[0].version
__title__ = 'flake8_tensors'
__summary__ = 'flake8_tensors - flake8 plugin for deep learning codes'
__license__ = 'MIT'
__author__ = 'David Völgyes'
__email__ = 'david.volgyes@ieee.org'
__description__ = """
This program is a flake8 plugin, and recommends some tricks
and best practices for machine learning codes.
"""

from .plugin import Flake8TensorsPlugin

__all__ = ['Flake8TensorsPlugin']
