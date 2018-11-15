#!/usr/bin/env bash

# https://nose.readthedocs.io/en/latest/usage.html
cd test
export PYTHONPATH="."
nosetests

# nosetests --verbosity=1

