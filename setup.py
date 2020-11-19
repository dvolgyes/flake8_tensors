#!/usr/bin/env python

import setuptools
import flake8_tensors as f8tensors

setuptools.setup(
    name=f8tensors.__title__,
    version=f8tensors.__version__,
    author=f8tensors.__author__,
    author_email=f8tensors.__email__,
    description=f8tensors.__summary__,
    description_content_type='text/plain',
    long_description=f8tensors.__description__,
    long_description_content_type='text/markdown',
    url=f8tensors.__uri__,
    license=f8tensors.__license__,
    packages=["flake8_tensors",],
    entry_points={
        'flake8.extension': ['WT = flake8_tensors:Flake8TensorsPlugin',],
        },
    python_requires='>=3.6',
    setup_requires=['flake8', 'importlib', 'bidict', 'pyyaml','importlib-metadata', 'astpath'],
    install_requires=['flake8', 'importlib', 'bidict', 'pyyaml','importlib-metadata', 'astpath'],
    keywords='flake8 pytorch',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
    ],
)
