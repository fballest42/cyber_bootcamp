#!/bin/bash
python -m pip install --upgrade build
python -m pip install --upgrade pip setuptools wheel
python -m build && pip install ./dist/my_minipack-1.0.0-py3-none-any.whl
pip install ./dist/my_minipack-1.0.0.tar.gz
