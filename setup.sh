#!/bin/sh

python3 -m venv  ~/.venvs/npyi
. ~/.venvs/npyi/bin/activate
pip install -r requirements.txt
pre-commit install
