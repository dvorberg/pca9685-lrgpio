#!/bin/bash

if [ "!" -d pca9685 ]
then
    echo "Must be run in project home."
    exit 255
fi

rm -R -f doc/*

. .virtualenv.$(hostname -s)/bin/activate 

PYTHONPATH=. pdoc -n -o doc/ -d google \
             --no-include-undocumented \
             --no-search \
             pca9685
