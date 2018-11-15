#!/usr/bin/env bash

# https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure


cd test
export PYTHONPATH="../src:."
python -m unittest discover
